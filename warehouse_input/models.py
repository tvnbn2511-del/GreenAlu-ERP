from django.db import models
from django.utils import timezone
class MaterialCategory(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã nhóm")
    name = models.CharField(max_length=200, verbose_name="Tên nhóm")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Nhóm vật tư"
        verbose_name_plural = "Nhóm vật tư"
# 1. Loại vật tư (Phải đứng đầu)
class MaterialType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên loại vật tư")
    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.SET_NULL, # Nếu xóa nhóm, vật tư không bị xóa (chỉ mất nhóm)
        null=True,                 # Cho phép cũ chưa có nhóm
        blank=True,
        related_name='material_types',
        verbose_name="Thuộc nhóm"
    )
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã VT")
    unit = models.CharField(max_length=20, default="kg", verbose_name="Đơn vị")
    description = models.TextField(blank=True, verbose_name="Mô tả")

    def __str__(self): return f"{self.name} ({self.code})"

# 2. Nhà cung cấp
class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nhà cung cấp")
    phone = models.CharField(max_length=20, blank=True, verbose_name="SĐT")
    address = models.TextField(blank=True, verbose_name="Địa chỉ")
    
    def __str__(self): return self.name

# 3. Phiếu nhập (Header)
class InputVoucher(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã phiếu nhập")
    date = models.DateTimeField(default=timezone.now, verbose_name="Ngày nhập")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name="Nhà cung cấp")
    note = models.TextField(blank=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.code} - {self.supplier.name}"

    @property
    def total_amount(self):
        # Tính tổng tiền (Cần InputVoucherDetail đã được định nghĩa hoặc dùng related name)
        # Lưu ý: Hàm này gọi lúc chạy (runtime) nên đặt ở đây vẫn OK
        return sum(item.total_price for item in self.details.all())

# 4. Chi tiết phiếu nhập (Detail)
class InputVoucherDetail(models.Model):
    voucher = models.ForeignKey(InputVoucher, related_name='details', on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialType, on_delete=models.PROTECT, verbose_name="Loại hàng")
    
    supplier_lot_no = models.CharField(max_length=50, blank=True, verbose_name="Lot NCC") 
    quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Khối lượng (kg)")
    unit_price = models.DecimalField(max_digits=14, decimal_places=2, default=0, verbose_name="Đơn giá (VND)") 
    
    # QC Input
    si_test = models.FloatField(default=0, verbose_name="Si (%)")
    fe_test = models.FloatField(default=0, verbose_name="Fe (%)")
    cu_test = models.FloatField(default=0, verbose_name="Cu (%)")

    def __str__(self): return f"{self.material_type.code} - {self.quantity}kg"

    @property
    def total_price(self):
        return self.quantity * self.unit_price