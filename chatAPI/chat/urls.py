from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ChatAPIView, chatbot, delete_chat

router = DefaultRouter()
router.register('', ChatAPIView)
urlpatterns = [
    path('model/', include(router.urls)),
    path('api/', chatbot, name='chatbot'),
    path('delete/', delete_chat, name='delete_chat')
]

