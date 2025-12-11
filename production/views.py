# production/views.py

from rest_framework import viewsets
from .models import FinishedBundle, Customer, ProductionBatch
from .serializers import FinishedBundleSerializer, CustomerSerializer, ProductionBatchSerializer

class FinishedBundleViewSet(viewsets.ModelViewSet):
    """
    API này cho phép xem, thêm, sửa, xóa các kiện hàng (FinishedBundle)
    """
    queryset = FinishedBundle.objects.all().order_by('-id') # Lấy tất cả, cái mới nhất lên đầu
    serializer_class = FinishedBundleSerializer
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
class ProductionBatchViewSet(viewsets.ModelViewSet):
    queryset = ProductionBatch.objects.all().order_by('-id')
    serializer_class = ProductionBatchSerializer    