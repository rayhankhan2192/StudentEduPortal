from django.db import models
from accountsapp.models import Account
import uuid


class Group(models.Model):
    group_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    admin = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="admin_groups")
    members = models.ManyToManyField(Account, related_name="group_members", blank=True)
    invite_code = models.UUIDField(default=uuid.uuid4, unique=True)

class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"
