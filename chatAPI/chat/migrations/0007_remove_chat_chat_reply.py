# Generated by Django 4.2.7 on 2023-11-27 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_remove_chatreply_chat_chat_chat_reply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='chat_reply',
        ),
    ]
