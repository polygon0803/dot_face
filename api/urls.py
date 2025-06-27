from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestItemViewSet, StatusCheckView, UserProfileAPIView

router = DefaultRouter()
router.register(r'testitems', TestItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('status/', StatusCheckView.as_view(), name='status_check'),
    path('user_profile/<str:user__username>/', UserProfileAPIView.as_view(), name='user_profile_api'),
]
