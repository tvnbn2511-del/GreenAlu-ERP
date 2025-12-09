from django.contrib import admin
from .models import InventoryItem, StockAdjustment

class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('material_type', 'quantity_on_hand', 'last_updated')
    list_filter = ('material_type',)

class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'material_type', 'adjustment_quantity', 'date')

admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(StockAdjustment, StockAdjustmentAdmin)