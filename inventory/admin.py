from django.contrib import admin
from .models import Product, ProductionBatch

# Đăng ký bảng Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

# Đăng ký bảng ProductionBatch
@admin.register(ProductionBatch)
class ProductionBatchAdmin(admin.ModelAdmin):
    list_display = ('lot_no', 'product', 'production_date')
