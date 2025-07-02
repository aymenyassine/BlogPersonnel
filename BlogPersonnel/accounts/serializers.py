from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=False)
    imageProfile = serializers.ImageField(required=False)
    imageCoverture = serializers.ImageField(required=False)
    role = serializers.CharField(read_only=True)
    etat = serializers.CharField(read_only=True)  

    class Meta:
        model = CustomUser
        fields = (
            'id','username', 'email', 'first_name', 'last_name', 
            'bio', 'imageProfile', 'imageCoverture', 'password','role','etat'
        )

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', ''),
        )

        # Ces champs ne doivent être assignés que s’ils sont présents.
        if 'imageProfile' in validated_data:
            user.imageProfile = validated_data['imageProfile']
        if 'imageCoverture' in validated_data:
            user.imageCoverture = validated_data['imageCoverture']

        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance