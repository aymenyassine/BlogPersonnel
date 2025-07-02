from rest_framework import serializers

from blog.serializers import SignalerSerializer
from .models import Ticket
from blog.models import Notification

class TicketSerializer(serializers.ModelSerializer):
    mark_as_resolved = serializers.BooleanField(
        write_only=True,
        required=False,
        label="Marquer comme résolu"
    )
    support_agent_username = serializers.CharField(source='support_agent.username', read_only=True)
    signalement = SignalerSerializer(read_only=True) 
    class Meta:
        model = Ticket
        fields = [
            'id', 'signalement', 'support_agent_username','support_agent', 'response', 
            'status', 'created_at', 'updated_at', 'mark_as_resolved'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def update(self, instance, validated_data):
        mark_as_resolved = validated_data.pop('mark_as_resolved', False)
        
        if mark_as_resolved:
            validated_data['status'] = 'Résolu'
        
        instance = super().update(instance, validated_data)
        
        # Création de la notification
        if instance.signalement:
            Notification.objects.get_or_create(
            user=instance.signalement.user,
            post=instance.signalement.post,
            defaults={
                'message': f"Votre signalement a été {instance.status} : {instance.response}"
                }
            )
        
        return instance