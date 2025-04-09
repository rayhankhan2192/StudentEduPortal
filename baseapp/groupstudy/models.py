from django.db import models
from accountsapp.models import Account
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class GroupStudy(models.Model):
    groupName = models.CharField(max_length=255, blank=False, null=False)  
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 
    is_active = models.BooleanField(default=True)
    auth_users = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='groupstudy')
    members = models.ManyToManyField(Account, related_name="studygroup_members", blank=True)
    invite_code = models.UUIDField(default=uuid.uuid4, unique=True)  
    last_message_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.groupName

def upload_to_group_files(instance, filename):
    return f'group_study/{instance.group.id}/{filename}'

class GroupStudyMessage(models.Model):
    group = models.ForeignKey(GroupStudy, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=upload_to_group_files, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.group.last_message_time = self.timestamp
        self.group.save()

    def __str__(self):
        return f'Message from {self.sender} in {self.group.groupName}'
    
