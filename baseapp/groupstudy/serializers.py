from .models import CreateGroup
from rest_framework import serializers


class CreateGroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = CreateGroup
        fields = ['id', 'groupName']