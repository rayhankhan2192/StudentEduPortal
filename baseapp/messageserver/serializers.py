from .models import *
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'group_name', 'admin', 'members', 'invite_code']
        read_only_fields = ['invite_code']
    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated.")
        user = request.user
        if Group.objects.filter(group_name = validated_data['group_name'], admin = user).exists():
            raise serializers.ValidationError({"message": "Group Name already exists."})
        validated_data['auth_users'] = user
        return super().create(validated_data)
        
class MessageSerializer(serializers.Serializer):
    class Meta:
        model = Message
        fields = ['id', 'group', 'sender', 'content', 'timestamp']