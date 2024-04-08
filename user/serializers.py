from rest_framework import serializers

from .models import User


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'last_name', 'email', 'nickname')

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('name', 'last_name', 'email', 'password', 'confirm_password')
    
    def validate(self, attrs):
        super().validate(attrs)
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("passwords don't match")
        return attrs

    def create(self, validated_data: dict):
        validated_data.pop('confirm_password')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
            'name': instance.name,
            'last_name': instance.last_name
        }