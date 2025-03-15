from django.db import models

class CreateGroup(models.Model):
    groupName = models.CharField(max_length=255, blank=False, null=False)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.groupName