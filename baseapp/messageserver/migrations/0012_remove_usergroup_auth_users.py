# Generated by Django 5.1.7 on 2025-04-10 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messageserver', '0011_alter_usergroup_auth_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergroup',
            name='auth_users',
        ),
    ]
