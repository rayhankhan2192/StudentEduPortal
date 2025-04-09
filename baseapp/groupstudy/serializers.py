from .models import GroupStudy
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class CreateGroupSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    class Meta:
        model = GroupStudy
        fields = ['id', 'groupName', 'password']
        
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
        

