from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from blog.models import Post, Like, Comment
from blog.serializers import PostSerializer
from Amis.models import Amis
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils.dateformat import DateFormat


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'user': UserSerializer(user).data,
                    'token': token.key
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f"Erreur d'inscription : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)

            user.etat = "En_ligne"
            user.save()

            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'role': user.role,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f"Erreur de connexion : {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            print(request.data)
            user = request.user
            user.etat = "Offline"
            user.save()
            user.auth_token.delete()
            return Response({"detail": "Déconnexion réussie."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f"Erreur de déconnexion : {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)


class GetAuthenticatedUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            search_query = request.query_params.get('search', '')

            posts = Post.objects.filter(author=user)
            if search_query:
                posts = posts.filter(title__icontains=search_query)
            posts = posts.order_by('-created_at')

            return Response({
                "user": UserSerializer(user).data,
                "posts": PostSerializer(posts, many=True).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f"Erreur lors de la récupération : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            serializer = UserSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f"Erreur de mise à jour : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllUsers(APIView):
    def get(self, request):
        try:
            users = CustomUser.objects.all()
            return Response(UserSerializer(users, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f"Erreur lors de la récupération des utilisateurs : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetUser(APIView):
    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'detail': "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f"Erreur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(APIView):
    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
            posts = Post.objects.filter(author=user)
            return Response({
                "user": UserSerializer(user).data,
                "posts": PostSerializer(posts, many=True).data
            }, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'detail': "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f"Erreur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            posts = Post.objects.filter(author=user)
            post_ids = posts.values_list('id', flat=True)

            top_categories = (
                posts.values('category__name')
                .annotate(count=Count('id'))
                .order_by('-count')[:3]
            )
            formatted_categories = [
                {"name": cat["category__name"], "count": cat["count"]}
                for cat in top_categories
            ]

            posts_per_month = (
                posts.annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(count=Count('id'))
                .order_by('month')
            )
            formatted_posts_per_month = [
                {"month": DateFormat(p['month']).format('Y-m'), "count": p["count"]}
                for p in posts_per_month
            ]

            likes_per_month = (
                Like.objects.filter(post_id__in=post_ids)
                .annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(count=Count('id'))
                .order_by('month')
            )
            formatted_likes_per_month = [
                {"month": DateFormat(l['month']).format('Y-m'), "count": l["count"]}
                for l in likes_per_month
            ]

            stats = {
                "posts": posts.count(),
                "likes": Like.objects.filter(post_id__in=post_ids).count(),
                "comments": Comment.objects.filter(post_id__in=post_ids).count(),
                "followers": Amis.objects.filter(recepteur=user, accepter=True).count() +
                             Amis.objects.filter(demandeur=user, accepter=True).count(),
                "topCategories": formatted_categories,
                "postsPerMonth": formatted_posts_per_month,
                "likesPerMonth": formatted_likes_per_month,
            }

            return Response(stats, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f"Erreur lors de la récupération des statistiques : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserPostViewsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            posts = Post.objects.filter(author=user).values('id', 'title', 'views')
            return Response({"posts": list(posts)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f"Erreur lors de la récupération des vues : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserTopViewedPostsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            top_posts = Post.objects.filter(author=user).order_by('-views')[:5]
            data = [
                {
                    "id": post.id,
                    "title": post.title,
                    "views": post.views,
                    "likes": post.likes.count(),
                    "created_at": post.created_at
                }
                for post in top_posts
            ]
            return Response({"topViewedPosts": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f"Erreur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'detail': 'Compte supprimé avec succès.'}, status=status.HTTP_204_NO_CONTENT)