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

class Chat(BaseModel):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  prompt = models.CharField(max_length=512)
  chat_reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='response', null=True)
  created_at = models.DateTimeField(auto_now_add=True)


