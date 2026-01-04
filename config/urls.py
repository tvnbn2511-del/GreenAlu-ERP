# config/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from production.views import FinishedBundleViewSet, CustomerViewSet, ProductionBatchViewSet, WeighingSlipViewSet, index, weighing
from warehouse_input.views import MaterialTypeViewSet, SupplierViewSet, InputVoucherViewSet
from warehouse_stock.views import InventoryItemViewSet, StockAdjustmentViewSet
from warehouse_stock.views import inventory_page  # <--- Để sửa lỗi inventory_page not defined
from warehouse_input.views import import_page     # <--- Để dùng được trang nhập kho
# Phần Production
router = DefaultRouter()
router.register(r'finished-bundles', FinishedBundleViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'batches', ProductionBatchViewSet)
router.register(r'weighing-slips', WeighingSlipViewSet)
#Phần NVL Đầu Vào
router.register(r'materials', MaterialTypeViewSet)      # Danh mục vật tư
router.register(r'suppliers', SupplierViewSet)          # Danh mục NCC
router.register(r'input-vouchers', InputVoucherViewSet) # Phiếu nhập kho
router.register(r'adjustments', StockAdjustmentViewSet) # Kiểm kê kho

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), # Đăng ký đường dẫn API
    path('', index, name='home'),
    path('can-hang/', weighing, name='weighing'),
    path('ton-kho/', inventory_page, name='inventory'), # Truy cập: /ton-kho/
    path('nhap-kho/', import_page, name='import'),      # Truy cập: /nhap-kho/
]