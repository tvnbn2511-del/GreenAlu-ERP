# config/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from production.views import FinishedBundleViewSet, CustomerViewSet, ProductionBatchViewSet, WeighingSlipViewSet, index, weighing
# Tạo Router
router = DefaultRouter()
router.register(r'finished-bundles', FinishedBundleViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'batches', ProductionBatchViewSet)
router.register(r'weighing-slips', WeighingSlipViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), # Đăng ký đường dẫn API
    path('', index, name='home'),
    path('can-hang/', weighing, name='weighing'),
]