from rest_framework import serializers
from .models import ECH, ECL

class OrderSerializer(serializers.Serializer):
  """Order Serializer"""
  HCUST = serializers.IntegerField(required=True)
  HSHOP = serializers.IntegerField(required=True)
  HPROD = serializers.JSONField(required=True)


class OrderInfoSerializer(serializers.ModelSerializer):
  """Order info"""
  class Meta:
    model = ECH
    fields = '__all__'


class OrderLineSerializer(serializers.Serializer):
  """Order line details serializer"""
  class Meta:
    model = ECL
    fields = '__all__'

    
