from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('chat/', include('chat.urls')),
    path('quote/', include('quote.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/login/', include('rest_social_auth.urls_jwt_pair')),
]

