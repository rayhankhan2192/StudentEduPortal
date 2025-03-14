from .models import *
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'username',
            'email',
            'role',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user
