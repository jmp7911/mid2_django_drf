from django import forms
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView

from .models import User
from django.db import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField, PasswordChangeForm
from django.contrib.auth import get_user_model

class UserJoinForm(UserCreationForm):
  password1 = forms.CharField(
    label='비밀번호',
    widget=forms.PasswordInput(
      attrs={'class': "form-control", "autocomplete": "password", 'placeholder': '비밀번호'}),
  )
  password2 = forms.CharField(
    label='비밀번호 확인',
    widget=forms.PasswordInput(
      attrs={'class': "form-control", "autocomplete": "password", 'placeholder': '비밀번호 확인'}),
  )
  class Meta:
    model = get_user_model()
    fields = ['email', 'nickname', 'profile_image' ]
    field_classes = {"email": UsernameField}
    widgets = {
      'email': forms.EmailInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Email을 입력하세요',
          'required': 'required',
        }),
      'nickname': forms.TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': '닉네임을 입력하세요',
          'required': 'required',
        }
      ),
      'profile_image': forms.ClearableFileInput(
        attrs={
          'class': 'form-control'
        }
      ),

    }
    
class UserProfileForm(UserChangeForm):
  
  class Meta:
    model = get_user_model()
    fields = ['email', 'nickname', 'profile_image']
    field_classes = {"email": UsernameField}
    widgets = {
      'email': forms.EmailInput(
      attrs={
        'class': 'form-control',
        'placeholder': 'Email을 입력하세요',
        'required': 'required',
        'readonly': 'readonly'
      }),
      'nickname': forms.TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': '닉네임을 입력하세요',
          'required': 'required',
        }
      ),
      'profile_image': forms.ClearableFileInput(
        attrs={
          'class': 'form-control'
        }
      )
    }

class UserPasswordChangeForm(PasswordChangeForm):
  old_password = forms.CharField(
    label='기존 비밀번호',
    widget=forms.PasswordInput(attrs={'class': "form-control", "autocomplete": "new-password", 'placeholder': '기존 비밀번호'}),
  )
  new_password1 = forms.CharField(
    label='새 비밀번호',
    widget=forms.PasswordInput(
      attrs={'class': "form-control", "autocomplete": "new-password", 'placeholder': '새 비밀번호'}),
  )
  new_password2 = forms.CharField(
    label='새 비밀번호 (확인)',
    widget=forms.PasswordInput(
      attrs={'class': "form-control", "autocomplete": "new-password", 'placeholder': '새 비밀번호 (확인)'}),
  )