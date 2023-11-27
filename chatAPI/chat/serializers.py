from rest_framework.serializers import ModelSerializer
from .models import Chat, ChatReply
class ChatReplySerializer(ModelSerializer):
  class Meta:
    model = ChatReply
    fields = '__all__'

class ChatSerializer(ModelSerializer):
  chat_reply = ChatReplySerializer(required=True)
  class Meta:
    model = Chat
    fields = '__all__'

  def create(self, validated_data):
    chat_reply_data = validated_data.pop('chat_reply')
    chat_reply = ChatReply.objects.create(**chat_reply_data)
    validated_data['chat_reply'] = chat_reply
    chat = Chat(**validated_data)
    chat.save()

    return chat
