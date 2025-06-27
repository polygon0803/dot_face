from rest_framework import serializers
from .models import TestItem

class TestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestItem
        fields = '__all__'
