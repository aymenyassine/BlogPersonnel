from django.db import models
from accounts.models import CustomUser
from blog.models import Signaler

class Ticket(models.Model):
    STATUS = [
        ('Résolu', 'Résolu'),
        ('En_cours', 'En_cours'),
        ('Refusé', 'Refusé')
    ]
    signalement = models.OneToOneField(Signaler, on_delete=models.CASCADE)
    support_agent = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    response = models.TextField(blank=True, null=True)
    status =  models.CharField(max_length=50,choices=STATUS,default='En_cours')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket pour {self.signalement.objet} (par {self.signalement.user.username})"