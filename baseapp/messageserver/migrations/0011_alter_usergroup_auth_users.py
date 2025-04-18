# Generated by Django 5.1.7 on 2025-04-10 20:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messageserver', '0010_alter_usergroup_auth_users'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergroup',
            name='auth_users',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createusergroup', to=settings.AUTH_USER_MODEL),
        ),
    ]
