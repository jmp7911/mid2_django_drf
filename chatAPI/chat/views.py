from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Chat
from .serializers import ChatSerializer


class ChatAPIView(ModelViewSet):
  queryset = Chat.objects.all()
  serializer_class = ChatSerializer


