# Generated by Django 4.2.7 on 2023-11-27 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_remove_chat_chat_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='chat_reply',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='chat.chatreply'),
            preserve_default=False,
        ),
    ]
