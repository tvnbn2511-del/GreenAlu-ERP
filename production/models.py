from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from warehouse_input.models import InputVoucherDetail, MaterialType

# ==============================================================================
# 1. DANH MỤC CƠ BẢN (KHÁCH HÀNG, MÁC NHÔM, TIÊU CHUẨN)
# ==============================================================================

class Customer(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã KH")
    name = models.CharField(max_length=200, verbose_name="Tên Khách Hàng")
    def __str__(self): return self.name

class AlloyType(models.Model):
    """
    DANH MỤC MÁC NHÔM (MASTER DATA)
    VD: ADC12, A356, 6063...
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="Tên Mác Nhôm")
    description = models.TextField(blank=True, verbose_name="Mô tả đặc tính")

    def __str__(self): return self.name

class ProductStandard(models.Model):
    """
    Tiêu chuẩn sản phẩm theo từng Khách hàng & Mác nhôm
    """
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã Tiêu chuẩn")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Khách hàng")
    
    # --- THAY ĐỔI: Chọn từ danh sách Mác nhôm ---
    alloy_type = models.ForeignKey(AlloyType, on_delete=models.PROTECT, verbose_name="Mác nhôm áp dụng")
    
    # Thành phần hóa học yêu cầu
    si_min = models.FloatField(default=0, verbose_name="Si Min")
    si_max = models.FloatField(default=0, verbose_name="Si Max")
    fe_min = models.FloatField(default=0, verbose_name="Fe Min")
    fe_max = models.FloatField(default=0, verbose_name="Fe Max")
    cu_min = models.FloatField(default=0, verbose_name="Cu Min")
    cu_max = models.FloatField(default=0, verbose_name="Cu Max")
    # ... Bạn có thể thêm Mg, Mn, Zn, Ni ...
    
    notes = models.TextField(blank=True, verbose_name="Quy cách tem/đóng gói")

    class Meta:
        unique_together = ('customer', 'alloy_type') # Mỗi KH chỉ có 1 tiêu chuẩn cho 1 loại mác nhôm

    def __str__(self): return f"{self.alloy_type.name} - {self.customer.code}"


# ==============================================================================
# 2. KẾ HOẠCH & LỆNH SẢN XUẤT (TRUNG TÂM LOTNO)
# ==============================================================================

class MonthlyPlan(models.Model):
    month = models.CharField(max_length=7, verbose_name="Tháng (YYYY-MM)") 
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE, verbose_name="Loại vật tư")
    planned_quantity = models.FloatField(default=0, verbose_name="Kế hoạch (Kg)")
    
    class Meta:
        unique_together = ('month', 'material_type')

    def __str__(self): return f"Plan {self.month} - {self.material_type.name}"

class ProductionOrder(models.Model):
    """
    Lệnh Sản Xuất
    """
    lot_no = models.CharField(max_length=50, unique=True, verbose_name="LOT NO (Mã Lô)") 
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name="Khách hàng")
    
    # --- THAY ĐỔI: Chọn Mác nhôm từ danh sách ---
    product_type = models.ForeignKey(AlloyType, on_delete=models.PROTECT, verbose_name="Sản phẩm (Mác nhôm)")
    
    # Tiêu chuẩn sẽ tự động link theo KH + Mác nhôm (hoặc chọn thủ công nếu muốn override)
    standard = models.ForeignKey(ProductStandard, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tiêu chuẩn áp dụng")
    
    target_quantity = models.FloatField(default=0, verbose_name="Sản lượng yêu cầu (Kg)")
    date_created = models.DateTimeField(default=timezone.now, verbose_name="Ngày lập lệnh")
    
    status = models.CharField(max_length=20, choices=[
        ('NEW', 'Mới tạo'), 
        ('PROCESSING', 'Đang sản xuất'), 
        ('DONE', 'Đã đóng Lô')
    ], default='NEW')
    
    note = models.TextField(blank=True, verbose_name="Ghi chú SX")

    def __str__(self): return f"{self.lot_no} ({self.product_type.name})"

class ProductionOrderItem(models.Model):
    production_order = models.ForeignKey(ProductionOrder, related_name='items', on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialType, on_delete=models.PROTECT, verbose_name="Loại liệu cần")
    quantity_required = models.FloatField(verbose_name="Khối lượng cần (Kg)")
    
    def __str__(self): return f"{self.production_order.lot_no} - {self.material_type.name}"


# ==============================================================================
# 3. KHO: PHIẾU CÂN / SOẠN HÀNG (LIÊN KẾT VỚI LOTNO)
# ==============================================================================

class MaterialIssueDetail(models.Model):
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE, related_name='material_issues', verbose_name="Thuộc LotNo")
    source_input = models.ForeignKey(InputVoucherDetail, on_delete=models.PROTECT, verbose_name="Lấy từ Lô Nhập")
    real_weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="KL Thực (Kg)")
    
    status = models.CharField(max_length=20, choices=[
        ('WAITING', 'Đã cân/Chờ lò'), 
        ('CHARGED', 'Đã nạp lò'),
        ('RETURN', 'Trả lại kho')
    ], default='WAITING')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"Lot {self.production_order.lot_no} - {self.real_weight}kg"


# ==============================================================================
# 4. LÒ: NHẬT KÝ SẢN XUẤT (GẮN VỚI LOTNO)
# ==============================================================================

class ProductionBatch(models.Model):
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.PROTECT, related_name='batches', verbose_name="Sản xuất cho LotNo")
    furnace_name = models.CharField(max_length=50, verbose_name="Lò nấu")
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('COOKING', 'Đang nấu'), ('DONE', 'Hoàn thành')], default='COOKING')
    
    si_final = models.FloatField(default=0, verbose_name="Si Final")
    fe_final = models.FloatField(default=0, verbose_name="Fe Final")
    cu_final = models.FloatField(default=0, verbose_name="Cu Final")
    
    history = HistoricalRecords()

    def __str__(self): return f"{self.production_order.lot_no} @ {self.furnace_name}"

class FurnaceLog(models.Model):
    batch = models.ForeignKey(ProductionBatch, related_name='logs', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    action_type = models.CharField(max_length=20, choices=[('ADD', 'Nạp Liệu'), ('TEST', 'Test Mẫu')], default='ADD')
    
    issue_detail = models.ForeignKey(MaterialIssueDetail, on_delete=models.SET_NULL, null=True, blank=True)
    adhoc_material = models.ForeignKey(MaterialType, on_delete=models.SET_NULL, null=True, blank=True)
    adhoc_weight = models.FloatField(default=0)
    temperature = models.FloatField(default=0, verbose_name="Nhiệt độ")
    test_result_note = models.TextField(blank=True, verbose_name="KQ Test")


# ==============================================================================
# 5. THÀNH PHẨM & XUẤT HÀNG
# ==============================================================================

class WeighingSlip(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã phiếu cân TP")
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.PROTECT, verbose_name="Cân cho LotNo")
    date = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True)

    def __str__(self): return f"{self.code} - {self.production_order.lot_no}"

class FinishedBundle(models.Model):
    weighing_slip = models.ForeignKey(WeighingSlip, related_name='bundles', on_delete=models.CASCADE)
    barcode = models.CharField(max_length=100, unique=True, verbose_name="Mã vạch")
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="KL Tịnh")
    is_odd = models.BooleanField(default=False, verbose_name="Kiện lẻ")
    status = models.CharField(max_length=20, default='NEW', choices=[('NEW', 'Tồn kho'), ('SOLD', 'Đã bán')])
    batch = models.ForeignKey(ProductionBatch, on_delete=models.SET_NULL, null=True, blank=True)

class ScrapReturn(models.Model):
    weighing_slip = models.ForeignKey(WeighingSlip, related_name='scraps', on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialType, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

class DeliveryNote(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã phiếu xuất")
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name="Khách hàng")
    date = models.DateTimeField(default=timezone.now, verbose_name="Ngày xuất")
    note = models.TextField(blank=True)
    bundles = models.ManyToManyField(FinishedBundle, related_name='deliveries', verbose_name="Danh sách kiện")
    def __str__(self): return self.code

class RepackingSession(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã phiếu xử lý")
    date = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True)
    input_bundles = models.ManyToManyField(FinishedBundle, related_name='repacked_in', verbose_name="Kiện nguồn")
    def __str__(self): return self.code