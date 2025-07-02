from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q
from django.contrib.auth import get_user_model

from accounts.models import CustomUser
from .models import Amis, Chat
from .serializers import AmisSerializer, ChatSerializer
from accounts.serializers import UserSerializer
from blog.models import Notification
from rest_framework.parsers import MultiPartParser, FormParser

User = get_user_model()

# Vue pour envoyer une demande d'ami
class AmisRequestCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        demandeur = request.user
        try:
            recepteur = User.objects.get(id=user_id)

            if demandeur == recepteur:
                return Response({"detail": "Impossible d'envoyer une demande à soi-même."}, status=status.HTTP_400_BAD_REQUEST)

            if Amis.objects.filter(Q(demandeur=demandeur, recepteur=recepteur) | Q(demandeur=recepteur, recepteur=demandeur)).exists():
                return Response({"detail": "Une demande existe déjà."}, status=status.HTTP_400_BAD_REQUEST)

            Amis.objects.create(demandeur=demandeur, recepteur=recepteur)
            Notification.objects.create(user=recepteur, message=f"Demande d'amitié de {demandeur.username}")
            return Response({"detail": "Demande envoyée."}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"detail": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": f"Erreur inattendue : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Vue pour accepter ou refuser une demande
class AmisRequestResponseAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, action):
        try:
            demande = Amis.objects.get(pk=pk, recepteur=request.user)

            if action == 'accept':
                demande.accepter = True
                demande.save()
                Notification.objects.create(user=demande.demandeur, message=f"{request.user.username} a accepté votre demande d'ami")
                return Response({"detail": "Demande acceptée."})

            elif action == 'reject':
                demande.delete()
                return Response({"detail": "Demande rejetée."})

            return Response({"detail": "Action invalide."}, status=status.HTTP_400_BAD_REQUEST)

        except Amis.DoesNotExist:
            return Response({"detail": "Demande non trouvée."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": f"Erreur inattendue : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AmisListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            amis_relations = Amis.objects.filter((Q(demandeur=user) | Q(recepteur=user)) & Q(accepter=True))
            amis = [rel.recepteur if rel.demandeur == user else rel.demandeur for rel in amis_relations]
            serializer = UserSerializer(amis, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"detail": f"Erreur inattendue : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AmisDamisAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)

            is_friend = Amis.objects.filter(
                Q(demandeur=request.user, recepteur=target_user, accepter=True) |
                Q(demandeur=target_user, recepteur=request.user, accepter=True)
            ).exists()

            if not is_friend:
                return Response({"detail": "Non autorisé à voir ses amis."}, status=status.HTTP_403_FORBIDDEN)

            relations = Amis.objects.filter(
                (Q(demandeur=target_user) | Q(recepteur=target_user)) & Q(accepter=True)
            )
            amis = [rel.recepteur if rel.demandeur == target_user else rel.demandeur for rel in relations]
            serializer = UserSerializer(amis, many=True)
            return Response(serializer.data)

        except User.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": f"Erreur serveur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AmisDemandesRecuesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            demandes_recues = Amis.objects.filter(recepteur=request.user, accepter=False)
            serializer = AmisSerializer(demandes_recues, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": f"Erreur serveur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChatListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            chats = Chat.objects.filter(Q(user_send=user) | Q(user_recive=user)).order_by('-time_at')
            serializer = ChatSerializer(chats, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"detail": f"Erreur serveur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ChatCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, id_recevoir):
        user_send = request.user
        try:
            user_recive = CustomUser.objects.get(id=id_recevoir)
            data = request.data.copy()
            serializer = ChatSerializer(data=data)

            if serializer.is_valid():
                sont_amis = Amis.objects.filter(
                    ((Q(demandeur=user_send) & Q(recepteur=user_recive)) | 
                     (Q(demandeur=user_recive) & Q(recepteur=user_send))) &
                    Q(accepter=True)
                ).exists()

                if not sont_amis and Chat.objects.filter(user_send=user_send, user_recive=user_recive).count() >= 3:
                    return Response({"detail": "Non-amis. Limite de 3 messages atteinte."}, status=status.HTTP_403_FORBIDDEN)

                chat = serializer.save(user_send=user_send, user_recive=user_recive)
                Notification.objects.create(user=user_recive, message=f"Nouveau message de {user_send.username}")
                return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({"detail": "Utilisateur destinataire introuvable."}, status=status.HTTP_404_NOT_FOUND)



class ChatMarkAsReadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id_user):
        try:
            user = request.user
            user_autre = CustomUser.objects.get(id=id_user)
            chats = Chat.objects.filter(user_send=user_autre, user_recive=user, lue=False)
            updated = chats.update(lue=True)
            return Response({"detail": f"{updated} messages marqués comme lus."}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"detail": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": f"Erreur serveur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllUsers(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            demandes_existantes = Amis.objects.filter(Q(demandeur=user) | Q(recepteur=user))
            users_exclus = {user.id}
            for relation in demandes_existantes:
                users_exclus.add(relation.demandeur.id)
                users_exclus.add(relation.recepteur.id)

            utilisateurs_disponibles = CustomUser.objects.exclude(id__in=users_exclus)
            serializer = UserSerializer(utilisateurs_disponibles, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"detail": f"Erreur serveur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConversationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id_ami):
        try:
            user = request.user
            ami = CustomUser.objects.get(id=id_ami)

            messages = Chat.objects.filter(
                (Q(user_send=user) & Q(user_recive=ami)) |
                (Q(user_send=ami) & Q(user_recive=user))
            ).order_by('time_at')

            serializer = ChatSerializer(messages, many=True)
            return Response(serializer.data)

        except CustomUser.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": f"Erreur serveur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PeopleToFollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            amis_ids = Amis.objects.filter(
                Q(demandeur=user) | Q(recepteur=user),
                accepter=True
            ).values_list('demandeur', 'recepteur')

            amis_ids = set(sum(amis_ids, ()))
            suggestions = CustomUser.objects.exclude(id__in=amis_ids).exclude(id=user.id)[:5]
            serializer = UserSerializer(suggestions, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"detail": f"Erreur serveur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SentInvitationsList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            invitations = Amis.objects.filter(
                demandeur=request.user,
                accepter=False
            ).select_related('recepteur')

            serializer = AmisSerializer(invitations, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"detail": f"Erreur serveur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
