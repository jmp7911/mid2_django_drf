from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

from django.conf import settings
from django.utils.safestring import mark_safe


class CustomUserManager(UserManager):
  def _create_user(self, email, password, **extra_fields):
    if not email:
      raise ValueError('이메일은 필수입니다.')
    email = self.normalize_email(email)
    user = self.model(
      email=email,
      **extra_fields,
    )

    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(email, password, **extra_fields)

  def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    if extra_fields.get('is_staff') is not True:
      raise ValueError('superuser는 is_staff=True이어야 합니다.')
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('superuser는 is_superuser=True이어야 합니다.')

    return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
  # DB에 저장할 데이터를 선언
  username = models.CharField("사용자 계정", max_length=20, blank=True, null=True)
  password = models.CharField("비밀번호", max_length=128)  # 해시되기 때문에 max_length가 길어야함
  email = models.EmailField("이메일", max_length=50, unique=True)
  nickname = models.CharField("닉네임", max_length=50)

  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)

  ip_address = models.GenericIPAddressField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  profile_image = models.ImageField("프로필 사진", upload_to='account/%Y/%m/%d/', null=True, blank=True)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'

  def __str__(self):
    return self.email

  def get_short_name(self):
    return self.email

  def get_full_name(self):
    return self.email

  def get_image_tag(self):
    if not self.profile_image:
      return mark_safe(u'<img class="profile_image" src="%s" width="300"/>' % settings.DEFAULT_PROFILE_PATH)
    else:
      return mark_safe(u'<img class="profile_image" src="%s" width="300"/>' % self.profile_image.url)

  class Meta:
    verbose_name = '사용자'
    verbose_name_plural = '사용자'