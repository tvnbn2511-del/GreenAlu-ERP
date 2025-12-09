from django.contrib import admin
from .models import Customer, ProductStandard, ProductionBatch, FurnaceLog, WeighingSlip, FinishedBundle, ScrapReturn

class FurnaceLogInline(admin.TabularInline):
    model = FurnaceLog
    extra = 1

class ProductionBatchAdmin(admin.ModelAdmin):
    inlines = [FurnaceLogInline]
    list_display = ('lot_no', 'furnace_name', 'status')

class FinishedBundleInline(admin.TabularInline):
    model = FinishedBundle
    extra = 1

class ScrapReturnInline(admin.TabularInline):
    model = ScrapReturn
    extra = 1

class WeighingSlipAdmin(admin.ModelAdmin):
    inlines = [FinishedBundleInline, ScrapReturnInline]
    list_display = ('code', 'batch', 'date')

class FinishedBundleAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'weight', 'is_odd', 'status')
    list_filter = ('status', 'is_odd')
# ... (Import thêm DeliveryNote, RepackingSession) ...
from .models import DeliveryNote, RepackingSession

class DeliveryNoteAdmin(admin.ModelAdmin):
    list_display = ('code', 'customer', 'date')
    filter_horizontal = ('bundles',) # Giúp chọn kiện hàng dễ hơn (giao diện 2 khung trái phải)

class RepackingSessionAdmin(admin.ModelAdmin):
    list_display = ('code', 'date')
    filter_horizontal = ('input_bundles',)

admin.site.register(DeliveryNote, DeliveryNoteAdmin)
admin.site.register(RepackingSession, RepackingSessionAdmin)
admin.site.register(Customer)
admin.site.register(ProductStandard)
admin.site.register(ProductionBatch, ProductionBatchAdmin)
admin.site.register(WeighingSlip, WeighingSlipAdmin)
admin.site.register(FinishedBundle, FinishedBundleAdmin)