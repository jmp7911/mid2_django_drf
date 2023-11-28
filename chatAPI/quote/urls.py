from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import QuoteAPIView

router = DefaultRouter()
router.register('', QuoteAPIView)
urlpatterns = [
    path('', include(router.urls)),
]

