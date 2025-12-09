from django.db import models
from django.utils import timezone

class InventoryItem(models.Model):
    # Dùng chuỗi tham chiếu để tránh lỗi Circular Import
    material_type = models.ForeignKey('warehouse_input.MaterialType', on_delete=models.CASCADE, verbose_name="Loại vật tư")
    quantity_on_hand = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Tồn kho thực tế")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.material_type.name}: {self.quantity_on_hand}"

# ================= MỚI THÊM: KIỂM KÊ KHO =================
class StockAdjustment(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã phiếu kiểm kê")
    date = models.DateTimeField(default=timezone.now)
    material_type = models.ForeignKey('warehouse_input.MaterialType', on_delete=models.PROTECT, verbose_name="Vật tư")
    
    # Số lượng điều chỉnh: Có thể âm hoặc dương
    adjustment_quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Lượng điều chỉnh (+/-)")
    reason = models.TextField(verbose_name="Lý do chênh lệch")

    def __str__(self): return f"{self.code} ({self.adjustment_quantity}kg)"