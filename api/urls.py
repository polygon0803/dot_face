from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestItemViewSet

router = DefaultRouter()
router.register(r'testitems', TestItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
