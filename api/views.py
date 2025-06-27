from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TestItem
from .serializers import TestItemSerializer

class TestItemViewSet(viewsets.ModelViewSet):
    queryset = TestItem.objects.all()
    serializer_class = TestItemSerializer

class StatusCheckView(APIView):
    def get(self, request, format=None):
        return Response({"status": "DRF is working!"})
