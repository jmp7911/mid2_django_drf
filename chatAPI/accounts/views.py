from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth import authenticate, get_user_model
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserJoinForm, UserProfileForm, UserPasswordChangeForm
from .models import User

class PageTitleViewMixin:
  title = ""

  def get_title(self):
    return self.title
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = self.get_title()
    return context
  
class JoinUser(PageTitleViewMixin, CreateView):
  title = '회원가입'
  template_name = 'accounts/join.html'
  success_url = settings.LOGIN_URL
  form_class = UserJoinForm
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['context'] = super().get_context_data(**kwargs)
    return context
  
class loginUser(PageTitleViewMixin, LoginView):
  title = '로그인'
  template_name = 'accounts/login.html'
  next_page = 'blog'#로그인 성공 페이지
  
logout = LogoutView.as_view(
    next_page = settings.LOGIN_URL,
)

class ProfileUser(PageTitleViewMixin, UpdateView):
  title = '회원정보'
  template_name = 'accounts/profile.html'
  success_url = reverse_lazy('blog')
  form_class = UserProfileForm
  def get_object(self):
    return self.request.user
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['context'] = super().get_context_data(**kwargs)
    return context
  
class PasswordChangeUser(PageTitleViewMixin, PasswordChangeView):
  title = '비밀번호 변경'
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm
  
class PasswordChangeDoneUser(PageTitleViewMixin, PasswordChangeDoneView):
  title = '비밀번호 변경 완료'
  template_name = 'accounts/password_change_done.html'
  
  
signup = JoinUser.as_view()
login = loginUser.as_view()
profile = login_required(ProfileUser.as_view())
password_change = login_required(PasswordChangeUser.as_view())
password_change_done = login_required(PasswordChangeDoneUser.as_view())