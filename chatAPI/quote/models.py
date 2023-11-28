import logging

from django.contrib.auth import get_user_model
from django.db import models

from django.urls import reverse
from abc import abstractmethod

User = get_user_model()

class BaseModel(models.Model):
  class Meta:
    abstract = True

  @abstractmethod
  def get_absolute_url(self):
    pass
class Tag(models.Model):
  name = models.CharField(max_length=100, unique=True)

  def __str__(self):
    return self.name


class Quote(BaseModel):
  title = models.CharField(max_length=100)
  content = models.TextField()
  description = models.CharField(max_length=512)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  applied_at = models.DateTimeField(auto_now=True)
  is_apply = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
  tags = models.ManyToManyField(Tag, blank=True)

  def __str__(self):
    return self.title
