# Generated by Django 4.2.7 on 2023-11-27 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_chat_chat_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='description',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='chat',
            name='quote',
            field=models.CharField(max_length=512, null=True),
        ),
    ]
