# Generated by Django 5.1.7 on 2025-04-09 15:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupstudy', '0009_groupstudy_members'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupstudy',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='studygroup_members', to=settings.AUTH_USER_MODEL),
        ),
    ]
