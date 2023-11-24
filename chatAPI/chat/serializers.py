from rest_framework.serializers import ModelSerializer
from .models import Chat
class ChatReplySerializer(ModelSerializer):
  class Meta:
    model = Chat
    fields = ['id', 'prompt', 'created_at']

class ChatSerializer(ModelSerializer):

  class Meta:
    model = Chat
    fields = '__all__'

