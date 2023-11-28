from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from .models import Quote, Tag

class UsernameSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ['email']
class QuoteSerializer(ModelSerializer):
  class Meta:
    model = Quote
    fields = '__all__'

class QuoteUserSerializer(ModelSerializer):
  user = UsernameSerializer()
  class Meta:
    model = Quote
    fields = '__all__'
