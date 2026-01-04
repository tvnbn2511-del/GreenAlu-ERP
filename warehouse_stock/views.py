from rest_framework import viewsets
from .models import InventoryItem, StockAdjustment
from .serializers import InventoryItemSerializer, StockAdjustmentSerializer
from django.shortcuts import render

class InventoryItemViewSet(viewsets.ReadOnlyModelViewSet): 
    # Dùng ReadOnly vì tồn kho nên được tính toán tự động, hạn chế sửa tay trực tiếp
    queryset = InventoryItem.objects.all().order_by('material_type__name')
    serializer_class = InventoryItemSerializer

class StockAdjustmentViewSet(viewsets.ModelViewSet):
    queryset = StockAdjustment.objects.all().order_by('-date')
    serializer_class = StockAdjustmentSerializer
def inventory_page(request):
    """Trả về giao diện báo cáo tồn kho"""
    return render(request, 'warehouse_stock/inventory.html')