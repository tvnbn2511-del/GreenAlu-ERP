from rest_framework import viewsets
from .models import MaterialType, Supplier, InputVoucher
from .serializers import MaterialTypeSerializer, SupplierSerializer, InputVoucherSerializer
from django.shortcuts import render

class MaterialTypeViewSet(viewsets.ModelViewSet):
    queryset = MaterialType.objects.all()
    serializer_class = MaterialTypeSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class InputVoucherViewSet(viewsets.ModelViewSet):
    # prefetch_related('details') giúp lấy luôn chi tiết, tránh query DB quá nhiều lần
    queryset = InputVoucher.objects.all().prefetch_related('details').order_by('-date')
    serializer_class = InputVoucherSerializer
def import_page(request):
    """Trả về giao diện phiếu nhập kho"""
    return render(request, 'warehouse_input/import.html')