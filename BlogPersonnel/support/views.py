# from django.shortcuts import render
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required, user_passes_test
# from blog.models import Notification
# from .models import Ticket
# from .forms import TicketResponseForm


# def is_support(user):
#     return user.is_staff or user.is_superuser

# @login_required
# @user_passes_test(is_support)
# def ticket_list(request):
#     tickets = Ticket.objects.all().order_by('-created_at')
#     return render(request, 'support/ticket_list.html', {'tickets': tickets})


# @login_required
# @user_passes_test(is_support)
# def ticket_detail(request, pk):
#     ticket = get_object_or_404(Ticket, pk=pk)
#     if request.method == 'POST':
#         form = TicketResponseForm(request.POST, instance=ticket)
#         if form.is_valid():
#             response_ticket = form.save(commit=False)
#             response_ticket.support_agent = request.user
#             response_ticket.save()

#             signal = ticket.signalement 
#             Notification.objects.create(
#                 user=signal.user,             
#                 post=signal.post,             
#                 message=f"Votre signalement a été {ticket.status} : {ticket.response}",
#                 is_read=False
#             )

#             return redirect('ticket_list')
#     else:
#         form = TicketResponseForm(instance=ticket)
    
#     return render(request, 'support/ticket_detail.html', {'ticket': ticket, 'form': form})


from venv import logger
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Ticket
from .serializers import TicketSerializer

class IsSupportUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related('signalement', 'signalement__user', 'signalement__post').order_by('-created_at')
    serializer_class = TicketSerializer
    permission_classes = [IsSupportUser]

    def update(self, request, *args, **kwargs):
        """
        PUT /tickets/{id}/
        Gère la mise à jour du ticket avec :
        - Assignation automatique de l'agent support
        - Gestion du statut
        - Envoi de notification
        """
        logger.debug(f"Request data: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Préparer les données avec l'agent support
        data = request.data.copy()
        if not instance.support_agent:
            data['support_agent'] = request.user.id

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Envoyer une notification si le statut ou la réponse a changé
        updated_instance = serializer.instance
        if any(field in request.data for field in ['status', 'response']):
            self.send_notification(updated_instance)

        return Response(serializer.data)

    def perform_update(self, serializer):
        """Sauvegarde avec l'utilisateur courant comme agent support si non défini"""
        if not serializer.instance.support_agent:
            serializer.save(support_agent=self.request.user)
        else:
            serializer.save()

    def send_notification(self, ticket):
        """Envoie une notification à l'utilisateur qui a signalé"""
        from blog.models import Notification
        
        if not ticket.signalement or not ticket.signalement.user:
            return

        status_display = ticket.get_status_display()
        message = (
            f"Votre signalement '{ticket.signalement.objet}' a été mis à jour. "
            f"Statut : {status_display}. "
            f"Réponse : {ticket.response or 'Aucune réponse fournie'}"
        )

        Notification.objects.get_or_create(
        user=ticket.signalement.user,
        post=ticket.signalement.post,
        defaults={
            'message': message,
            
        }
)