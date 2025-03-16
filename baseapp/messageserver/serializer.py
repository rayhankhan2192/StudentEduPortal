from .models import *
from rest_framework import serializers
from django.db.models import Q

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ['id', 'group_name', 'members', 'invite_code']
        read_only_fields = ['invite_code']
        
    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError({"message":"User must be authenticated."})
        user = request.user
        print("User:", user)
        if UserGroup.objects.filter(group_name = validated_data['group_name'], admin = request.user).exists():
            raise serializers.ValidationError({"message": "Group Name already exists."})
        validated_data['admin'] = user
        return super().create(validated_data)
        
class MessageSerializer(serializers.Serializer):
    class Meta:
        model = Message
        fields = ['id', 'group', 'sender', 'content', 'timestamp']