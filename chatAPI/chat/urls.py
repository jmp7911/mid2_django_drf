from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ChatAPIView

router = DefaultRouter()
router.register('', ChatAPIView)

urlpatterns = [
    path('', include(router.urls))
]

