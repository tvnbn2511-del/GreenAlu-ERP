from django.db import models
from django.utils import timezone
# Nếu lỗi "No module named simple_history", hãy chạy: pip install django-simple-history
# Hoặc comment 2 dòng dưới đây lại:
from simple_history.models import HistoricalRecords 

class InventoryItem(models.Model):
    # Dùng chuỗi tham chiếu 'warehouse_input.MaterialType' để tránh lỗi vòng lặp (Circular Import)
    material_type = models.ForeignKey('warehouse_input.MaterialType', on_delete=models.CASCADE, verbose_name="Loại vật tư")
    quantity_on_hand = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Tồn kho thực tế")
    min_stock_level = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Mức an toàn")
    
    last_updated = models.DateTimeField(auto_now=True)
    
    # Nếu chưa cài simple_history thì comment dòng này lại:
    history = HistoricalRecords() 

    def __str__(self):
        return f"{self.material_type.name}: {self.quantity_on_hand}"

class StockAdjustment(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã phiếu kiểm kê")
    date = models.DateTimeField(default=timezone.now)
    material_type = models.ForeignKey('warehouse_input.MaterialType', on_delete=models.PROTECT, verbose_name="Vật tư")
    
    adjustment_quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Lượng điều chỉnh (+/-)")
    reason = models.TextField(verbose_name="Lý do chênh lệch")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.code} ({self.adjustment_quantity}kg)"