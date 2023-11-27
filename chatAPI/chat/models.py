from abc import abstractmethod

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseModel(models.Model):
  class Meta:
    abstract = True

  @abstractmethod
  def get_absolute_url(self):
    pass



class ChatReply(BaseModel):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  quote = models.CharField(max_length=512)
  description = models.CharField(max_length=512)
  scene = models.CharField(max_length=512, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
class Chat(BaseModel):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  chat_reply = models.ForeignKey(ChatReply, on_delete=models.CASCADE)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
