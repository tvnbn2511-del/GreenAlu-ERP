from django.contrib import admin
from .models import MaterialType, Supplier, InputVoucher, InputVoucherDetail

class InputVoucherDetailInline(admin.TabularInline):
    model = InputVoucherDetail
    extra = 1

class InputVoucherAdmin(admin.ModelAdmin):
    list_display = ('code', 'date', 'supplier', 'created_at')
    inlines = [InputVoucherDetailInline]

admin.site.register(MaterialType)
admin.site.register(Supplier)
admin.site.register(InputVoucher, InputVoucherAdmin)