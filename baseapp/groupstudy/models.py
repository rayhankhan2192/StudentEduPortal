from django.db import models
from accountsapp.models import Account
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateGroup(models.Model):
    groupName = models.CharField(max_length=255, blank=False, null=False)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 
    is_active = models.BooleanField(default=True)
    auth_users = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='creategroup')

    def __str__(self):
        return self.groupName

