from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth.models import User
from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer
from .models import TestItem
from .serializers import TestItemSerializer

class TestItemViewSet(viewsets.ModelViewSet):
    queryset = TestItem.objects.all()
    serializer_class = TestItemSerializer

class StatusCheckView(APIView):
    def get(self, request, format=None):
        return Response({"status": "DRF is working!"})

class UserProfileAPIView(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user__username' # Look up by username