from rest_framework import viewsets
from .models import TestItem
from .serializers import TestItemSerializer

class TestItemViewSet(viewsets.ModelViewSet):
    queryset = TestItem.objects.all()
    serializer_class = TestItemSerializer