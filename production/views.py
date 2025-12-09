# production/views.py

from rest_framework import viewsets
from .models import FinishedBundle
from .serializers import FinishedBundleSerializer

class FinishedBundleViewSet(viewsets.ModelViewSet):
    """
    API này cho phép xem, thêm, sửa, xóa các kiện hàng (FinishedBundle)
    """
    queryset = FinishedBundle.objects.all().order_by('-id') # Lấy tất cả, cái mới nhất lên đầu
    serializer_class = FinishedBundleSerializer