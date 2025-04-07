from .models import CreateGroup
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class CreateGroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = CreateGroup
        fields = ['id', 'groupName', 'password']
        
    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError({"message":"User must be authenticated."})
        user = request.user
        if CreateGroup.objects.filter(groupName = validated_data['groupName'], auth_users = user).exists():
            raise serializers.ValidationError({"message": "Group Name already exists."})
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['auth_users'] = user
        return super().create(validated_data)
        

