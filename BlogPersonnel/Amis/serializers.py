from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Amis,Chat


class AmisSerializer(serializers.ModelSerializer):
    demandeur = UserSerializer(read_only=True)
    recepteur = UserSerializer(read_only=True)

    class Meta:
        model = Amis
        fields = ['id', 'demandeur', 'recepteur', 'time_at', 'accepter']

class ChatSerializer(serializers.ModelSerializer):
    user_send = UserSerializer(read_only=True)
    user_recive = UserSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'user_send', 'user_recive', 'msg','file','time_at', 'lue']