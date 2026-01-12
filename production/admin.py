from django.contrib import admin
from .models import (
    Customer, AlloyType, ProductStandard, 
    MonthlyPlan, ProductionOrder, ProductionOrderItem, MaterialIssueDetail, 
    ProductionBatch, FurnaceLog, 
    WeighingSlip, FinishedBundle, ScrapReturn,
    DeliveryNote, RepackingSession
)

# ========================================================
# 1. KẾ HOẠCH & ĐƠN HÀNG (TRUNG TÂM)
# ========================================================

class AlloyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class ProductStandardAdmin(admin.ModelAdmin):
    list_display = ('code', 'alloy_type', 'customer', 'si_min', 'si_max', 'fe_max')
    list_filter = ('alloy_type', 'customer')

class ProductionOrderItemInline(admin.TabularInline):
    model = ProductionOrderItem
    extra = 1

class MaterialIssueDetailInline(admin.TabularInline):
    model = MaterialIssueDetail
    fields = ('source_input', 'real_weight', 'status')
    readonly_fields = ('created_at',)
    extra = 0
    can_delete = False

class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = ('lot_no', 'product_type', 'target_quantity', 'customer', 'status', 'date_created')
    # Sửa lỗi: Dùng product_type thay vì product_name
    list_filter = ('status', 'customer', 'product_type') 
    search_fields = ('lot_no', 'customer__name')
    inlines = [ProductionOrderItemInline, MaterialIssueDetailInline]

# ========================================================
# 2. KHO (SOẠN HÀNG)
# ========================================================

class MaterialIssueDetailAdmin(admin.ModelAdmin):
    list_display = ('production_order', 'source_input', 'real_weight', 'status', 'created_at')
    
    # --- ĐÂY LÀ CHỖ GÂY LỖI TRƯỚC ĐÓ ---
    # Đã sửa: production_order__product_name -> production_order__product_type
    list_filter = ('status', 'production_order__product_type') 
    
    search_fields = ('production_order__lot_no',) 

# ========================================================
# 3. LÒ & SẢN XUẤT
# ========================================================

class FurnaceLogInline(admin.TabularInline):
    model = FurnaceLog
    extra = 1
    fields = ('timestamp', 'action_type', 'issue_detail', 'adhoc_material', 'adhoc_weight', 'temperature', 'test_result_note')

class ProductionBatchAdmin(admin.ModelAdmin):
    list_display = ('get_lot_no', 'furnace_name', 'status', 'start_time') 
    list_filter = ('status', 'furnace_name')
    search_fields = ('production_order__lot_no',) 
    inlines = [FurnaceLogInline]

    def get_lot_no(self, obj):
        return obj.production_order.lot_no if obj.production_order else "-"
    get_lot_no.short_description = 'Lot No'

# ========================================================
# 4. THÀNH PHẨM (ĐẦU RA)
# ========================================================

class FinishedBundleInline(admin.TabularInline):
    model = FinishedBundle
    extra = 1

class ScrapReturnInline(admin.TabularInline):
    model = ScrapReturn
    extra = 1

class WeighingSlipAdmin(admin.ModelAdmin):
    list_display = ('code', 'production_order', 'date', 'total_weight_display')
    search_fields = ('code', 'production_order__lot_no')
    inlines = [FinishedBundleInline, ScrapReturnInline]

    def total_weight_display(self, obj):
        total = sum([b.weight for b in obj.bundles.all()])
        return f"{total} kg"
    total_weight_display.short_description = "Tổng KL"

# ========================================================
# 5. CÁC DANH MỤC KHÁC
# ========================================================

class MonthlyPlanAdmin(admin.ModelAdmin):
    list_display = ('month', 'material_type', 'planned_quantity')
    list_filter = ('month',)

# ĐĂNG KÝ
admin.site.register(Customer)
admin.site.register(AlloyType, AlloyTypeAdmin)
admin.site.register(ProductStandard, ProductStandardAdmin)
admin.site.register(MonthlyPlan, MonthlyPlanAdmin)
admin.site.register(ProductionOrder, ProductionOrderAdmin)
admin.site.register(MaterialIssueDetail, MaterialIssueDetailAdmin)
admin.site.register(ProductionBatch, ProductionBatchAdmin)
admin.site.register(WeighingSlip, WeighingSlipAdmin)
admin.site.register(FinishedBundle)
admin.site.register(ScrapReturn)
admin.site.register(DeliveryNote)
admin.site.register(RepackingSession)