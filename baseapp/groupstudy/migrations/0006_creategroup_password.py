# Generated by Django 5.1.7 on 2025-04-07 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupstudy', '0005_remove_message_group_remove_message_sender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='creategroup',
            name='password',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
    ]
