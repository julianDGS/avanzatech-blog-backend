from rest_framework import serializers

from .models import User


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'last_name', 'email', 'nickname')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def create(self, validated_data: dict):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user