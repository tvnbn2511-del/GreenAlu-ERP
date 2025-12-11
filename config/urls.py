# config/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from production.views import FinishedBundleViewSet, CustomerViewSet, ProductionBatchViewSet

# Tạo Router
router = DefaultRouter()
router.register(r'finished-bundles', FinishedBundleViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'batches', ProductionBatchViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), # Đăng ký đường dẫn API
]