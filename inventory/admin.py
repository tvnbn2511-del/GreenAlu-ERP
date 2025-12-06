from django.contrib import admin
from .models import Product, ProductionBatch, Customer, Package

admin.site.register(Customer)
admin.site.register(Product)

# Cách hiển thị Phiếu cân ngay trong trang chi tiết của LotNo (Rất tiện!)
class PackageInline(admin.TabularInline):
    model = Package
    extra = 1 # Mặc định hiện sẵn 1 dòng trống để nhập

@admin.register(ProductionBatch)
class ProductionBatchAdmin(admin.ModelAdmin):
    list_display = ('lot_no', 'product', 'customer', 'production_date')
    list_filter = ('product', 'customer', 'production_date')
    # Thêm dòng này để nhập các kiện hàng ngay trong giao diện LotNo
    inlines = [PackageInline] 

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('batch', 'package_code', 'weight', 'created_at')
    list_filter = ('batch__lot_no',) # Lọc theo LotNo