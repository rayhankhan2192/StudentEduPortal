from .models import GroupStudy, GroupStudyMessage
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
User = get_user_model()

class CreateGroupSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    class Meta:
        model = GroupStudy
        fields = ['id', 'groupName', 'password', 'invite_code']
        
    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError({"message":"User must be authenticated."})
        user = request.user
        if GroupStudy.objects.filter(groupName = validated_data['groupName'], auth_users = user).exists():
            raise serializers.ValidationError({"message": "Group Name already exists."})
        password = validated_data.get('password', '')
        if password:
            validated_data['password'] = make_password(password)
        else:
            validated_data['password'] = ''
        validated_data['auth_users'] = user
        return super().create(validated_data)
        

class GroupStudyMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = GroupStudyMessage
        fields = ['id', 'group', 'sender', 'sender_name', 'text', 'file', 'timestamp']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError({"message":"User must be authenticated."})
        return GroupStudyMessage.objects.create(**validated_data)

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class GroupStudySerializer(serializers.ModelSerializer):
    latest_message = serializers.SerializerMethodField()
    auth_user_name = serializers.CharField(source='auth_users.username', read_only=True)
    members = UserMiniSerializer(many=True, read_only=True)  # <-- Update here
    class Meta:
        model = GroupStudy
        fields = [
            'id', 'groupName', 'password', 'created_at', 'updated_at', 'is_active',
            'auth_users', 'auth_user_name', 'members', 'invite_code',
            'last_message_time', 'latest_message'
        ]

    def get_latest_message(self, obj):
        latest = obj.messages.order_by('-timestamp').first()
        if latest:
            return GroupStudyMessageSerializer(latest).data
        return None