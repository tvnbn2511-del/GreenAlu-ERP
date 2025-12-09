from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

# 1. KHÁCH HÀNG & TIÊU CHUẨN
class Customer(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã KH")
    name = models.CharField(max_length=200, verbose_name="Tên Khách Hàng")
    def __str__(self): return self.name

class ProductStandard(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã Tiêu chuẩn")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Khách hàng")
    alloy_type = models.CharField(max_length=50, verbose_name="Mác nhôm")
    si_min = models.FloatField(default=0, verbose_name="Si Min")
    si_max = models.FloatField(default=0, verbose_name="Si Max")
    def __str__(self): return f"{self.code} ({self.customer.code})"

# 2. LÒ NẤU (MẺ)
class ProductionBatch(models.Model):
    lot_no = models.CharField(max_length=50, unique=True, verbose_name="Lot No")
    furnace_name = models.CharField(max_length=50, verbose_name="Lò nấu")
    target_standard = models.ForeignKey(ProductStandard, on_delete=models.SET_NULL, null=True, verbose_name="Tiêu chuẩn")
    date_started = models.DateTimeField(default=timezone.now, verbose_name="Bắt đầu")
    status = models.CharField(max_length=20, choices=[('COOKING', 'Đang nấu'), ('DONE', 'Hoàn thành')], default='COOKING')
    
    # Tổng kết
    total_slag = models.IntegerField(default=0, verbose_name="Xỉ (Gầu)")
    gas_usage = models.FloatField(default=0, verbose_name="Gas (kg)")
    history = HistoricalRecords()
    def __str__(self): return f"Lot {self.lot_no}"

# 3. NHẬT KÝ VẬN HÀNH (Furnace Log)
class FurnaceLog(models.Model):
    batch = models.ForeignKey(ProductionBatch, related_name='logs', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    action_type = models.CharField(max_length=10, choices=[('ADD', 'Nạp Liệu'), ('TEST', 'Test Mẫu')], verbose_name="Hành động")
    
    # Nếu nạp liệu (Dùng chuỗi tham chiếu sang app warehouse_input)
    material_type = models.ForeignKey('warehouse_input.MaterialType', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.FloatField(default=0, verbose_name="Khối lượng (kg)")
    
    # Nếu test mẫu
    si_result = models.FloatField(default=0, verbose_name="Si Result")
    note = models.TextField(blank=True)

# 4. ĐẦU RA (Phiếu cân)
class WeighingSlip(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã phiếu")
    batch = models.ForeignKey(ProductionBatch, on_delete=models.PROTECT, verbose_name="Thuộc LotNo")
    date = models.DateTimeField(default=timezone.now)
    def __str__(self): return self.code

class FinishedBundle(models.Model):
    weighing_slip = models.ForeignKey(WeighingSlip, related_name='bundles', on_delete=models.CASCADE)
    barcode = models.CharField(max_length=100, unique=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    is_odd = models.BooleanField(default=False, verbose_name="Kiện lẻ")
    status = models.CharField(max_length=20, default='NEW', choices=[('NEW', 'Mới'), ('SOLD', 'Đã bán')])
    batch = models.ForeignKey(ProductionBatch, on_delete=models.PROTECT, null=True) # Lưu dư để query nhanh

class ScrapReturn(models.Model):
    weighing_slip = models.ForeignKey(WeighingSlip, related_name='scraps', on_delete=models.CASCADE)
    material_type = models.ForeignKey('warehouse_input.MaterialType', on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
# ================= 5. XUẤT HÀNG (DELIVERY) =================
class DeliveryNote(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã phiếu xuất")
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name="Khách hàng")
    date = models.DateTimeField(default=timezone.now, verbose_name="Ngày xuất")
    note = models.TextField(blank=True)
    
    # Logic: Khi chọn kiện vào phiếu này -> Kiện đổi trạng thái thành SOLD
    bundles = models.ManyToManyField(FinishedBundle, related_name='deliveries', verbose_name="Danh sách kiện xuất")

    def __str__(self): return f"Xuất: {self.code} -> {self.customer.name}"

# ================= 6. TÁI CHẾ / GHÉP KIỆN (REPACKING) =================
class RepackingSession(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã phiếu xử lý")
    date = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True, verbose_name="Ghi chú (VD: Ghép 2 kiện lẻ)")
    
    # Đầu vào: Các kiện cũ bị xé ra (Chọn từ danh sách kiện đang có)
    input_bundles = models.ManyToManyField(FinishedBundle, related_name='repacked_in', verbose_name="Kiện nguồn (Bị hủy)")
    
    # Đầu ra: Chính là tạo FinishedBundle mới (Link vào batch cũ hoặc batch mới)
    
    def __str__(self): return self.code