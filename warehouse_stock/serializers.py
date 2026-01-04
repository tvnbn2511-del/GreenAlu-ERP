from rest_framework import serializers
from .models import InventoryItem, StockAdjustment

class InventoryItemSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material_type.name', read_only=True)
    material_code = serializers.CharField(source='material_type.code', read_only=True)
    unit = serializers.CharField(source='material_type.unit', read_only=True)

    class Meta:
        model = InventoryItem
        fields = ['id', 'material_type', 'material_name', 'material_code', 'quantity_on_hand', 'unit', 'last_updated']

class StockAdjustmentSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material_type.name', read_only=True)
    
    class Meta:
        model = StockAdjustment
        fields = '__all__'