from django.db import models
from accounts.models import CustomUser
from django.utils import timezone


class Amis(models.Model):
    demandeur = models.ForeignKey(CustomUser, related_name='demandeur_invitation', on_delete=models.CASCADE)
    recepteur = models.ForeignKey(CustomUser, related_name='recepteur_invitation', on_delete=models.CASCADE)
    time_at = models.DateTimeField(auto_now_add=True)
    accepter = models.BooleanField(default=False)

    class Meta:
        unique_together = ('demandeur', 'recepteur')

    def __str__(self):
        return f"{self.demandeur.username} -> {self.recepteur.username} | Accepted: {self.accepter}"


class Chat(models.Model):
    user_send = models.ForeignKey(CustomUser, related_name='user_send', on_delete=models.CASCADE)
    user_recive = models.ForeignKey(CustomUser, related_name='user_recive', on_delete=models.CASCADE)
    msg = models.TextField(max_length=1000, blank=True)
    file = models.FileField(upload_to='image/chat_image', null=True, blank=True)
    time_at = models.DateTimeField(default=timezone.now)
    lue = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_send.username} envoye un message à {self.user_recive.username}"

