# production/views.py
from rest_framework import viewsets
from .models import FinishedBundle, Customer, ProductionBatch, WeighingSlip
from .serializers import (
    FinishedBundleSerializer, 
    CustomerSerializer, 
    ProductionBatchSerializer, 
    WeighingSlipSerializer
)
from django.shortcuts import render

class ProductionBatchViewSet(viewsets.ModelViewSet):
    # SỬA LỖI Ở ĐÂY:
    # 1. Đổi '-date' thành '-date_started' (hoặc '-id')
    # 2. Đổi 'bundles' thành 'finishedbundle_set' nếu bạn chưa đặt related_name
    queryset = ProductionBatch.objects.all().prefetch_related('finishedbundle_set').order_by('-date_started')
    serializer_class = ProductionBatchSerializer

class FinishedBundleViewSet(viewsets.ModelViewSet):
    queryset = FinishedBundle.objects.all().order_by('-id')
    serializer_class = FinishedBundleSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class WeighingSlipViewSet(viewsets.ModelViewSet):
    queryset = WeighingSlip.objects.all().order_by('-id')
    serializer_class = WeighingSlipSerializer
def index(request):
    """Hàm này sẽ trả về file html giao diện chính"""
    return render(request, 'production/index.html')
def weighing(request):
    """Trả về giao diện phiếu cân"""
    return render(request, 'production/weighing.html')