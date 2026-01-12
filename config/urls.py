from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 1. IMPORT TỪ APP KHO (WAREHOUSE)
from warehouse_input.views import (
    MaterialTypeViewSet, 
    SupplierViewSet, 
    InputVoucherViewSet, 
    import_page
)
from warehouse_stock.views import (
    InventoryItemViewSet, 
    StockAdjustmentViewSet, 
    inventory_page
)

# 2. IMPORT TỪ APP SẢN XUẤT (PRODUCTION) - CẦN CẬP NHẬT ĐỦ Ở ĐÂY
from production.views import (
    ProductionOrderViewSet,      # <--- Cái bạn đang thiếu
    ProductionBatchViewSet,
    MaterialIssueDetailViewSet,  # <--- Cái mới thêm
    WeighingSlipViewSet,
    FinishedBundleViewSet,
    CustomerViewSet,
    ProductStandardViewSet,
    index, 
    weighing
)

router = DefaultRouter()

# --- ROUTER KHO ---
router.register(r'materials', MaterialTypeViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'input-vouchers', InputVoucherViewSet)
router.register(r'inventory', InventoryItemViewSet)
router.register(r'adjustments', StockAdjustmentViewSet)

# --- ROUTER SẢN XUẤT (MỚI) ---
router.register(r'production-orders', ProductionOrderViewSet)
router.register(r'batches', ProductionBatchViewSet)
router.register(r'material-issues', MaterialIssueDetailViewSet)
router.register(r'weighing-slips', WeighingSlipViewSet)
router.register(r'finished-bundles', FinishedBundleViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'standards', ProductStandardViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # Các trang HTML
    path('', index, name='home'),
    path('can-hang/', weighing, name='weighing'),
    path('ton-kho/', inventory_page, name='inventory'),
    path('nhap-kho/', import_page, name='import'),
]