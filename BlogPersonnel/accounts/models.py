from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE = [
        ('admin', 'admin'),
        ('user', 'user')
    ]
    STATUS =[
        ('En_ligne','En_ligne'),
        ('Offline','Offline')
    ]
    bio = models.CharField(max_length=255,blank=True,null=True)
    imageCoverture = models.ImageField(default='image/default.png',upload_to='image/imageCoverture')
    imageProfile = models.ImageField(default='image/default.png',upload_to='image/imageProfile')
    role =  models.CharField(max_length=50,choices=ROLE,default='user')
    etat = models.CharField(max_length=20,choices=STATUS,default='Offline')
    def __str__(self):
        return self.username
    