# Generated by Django 4.2.7 on 2023-11-27 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_remove_chat_chat_reply_remove_chat_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatreply',
            old_name='parent',
            new_name='chat',
        ),
        migrations.RemoveField(
            model_name='chatreply',
            name='content',
        ),
        migrations.AlterField(
            model_name='chatreply',
            name='scene',
            field=models.CharField(max_length=512, null=True),
        ),
    ]