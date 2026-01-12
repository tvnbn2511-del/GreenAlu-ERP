# production/views.py
from rest_framework import viewsets
from django.shortcuts import render

# Import Models
from .models import (
    ProductionOrder, ProductionBatch, MaterialIssueDetail,
    WeighingSlip, FinishedBundle, Customer, ProductStandard
)

# Import Serializers
from .serializers import (
    ProductionOrderSerializer, ProductionBatchSerializer, MaterialIssueDetailSerializer,
    WeighingSlipSerializer, FinishedBundleSerializer, CustomerSerializer, ProductStandardSerializer
)

# 1. View cho Lệnh Sản Xuất
class ProductionOrderViewSet(viewsets.ModelViewSet):
    # Sắp xếp theo ngày tạo mới nhất
    queryset = ProductionOrder.objects.all().order_by('-date_created')
    serializer_class = ProductionOrderSerializer

# 2. View cho Mẻ Nấu (Lò)
class ProductionBatchViewSet(viewsets.ModelViewSet):
    # LƯU Ý QUAN TRỌNG: Sửa date_started -> start_time
    queryset = ProductionBatch.objects.all().order_by('-start_time')
    serializer_class = ProductionBatchSerializer

# 3. View cho Kho Soạn Hàng
class MaterialIssueDetailViewSet(viewsets.ModelViewSet):
    queryset = MaterialIssueDetail.objects.all().order_by('-created_at')
    serializer_class = MaterialIssueDetailSerializer

# 4. View cho Thành Phẩm
class WeighingSlipViewSet(viewsets.ModelViewSet):
    queryset = WeighingSlip.objects.all().order_by('-date')
    serializer_class = WeighingSlipSerializer

class FinishedBundleViewSet(viewsets.ModelViewSet):
    queryset = FinishedBundle.objects.all().order_by('-id')
    serializer_class = FinishedBundleSerializer

# 5. Danh mục
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductStandardViewSet(viewsets.ModelViewSet):
    queryset = ProductStandard.objects.all()
    serializer_class = ProductStandardSerializer

# --- CÁC HÀM RENDER HTML CŨ (GIỮ NGUYÊN HOẶC CẬP NHẬT SAU) ---
def index(request):
    return render(request, 'production/index.html')

def weighing(request):
    return render(request, 'production/weighing.html')