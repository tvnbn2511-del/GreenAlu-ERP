from django.db import models
from django.utils import timezone

# 1. Danh mục Loại Vật Tư (VD: Phoi VX, Pitong...)
class MaterialType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên loại vật tư")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    unit = models.CharField(max_length=20, default="kg", verbose_name="Đơn vị tính")

    def __str__(self):
        return self.name

# 2. Nhà Cung Cấp
class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên nhà cung cấp")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Số điện thoại")
    address = models.TextField(blank=True, verbose_name="Địa chỉ")
    
    def __str__(self):
        return self.name

# 3. Phiếu Nhập (Header) - Chứa thông tin chung
class InputVoucher(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã phiếu")
    date = models.DateTimeField(default=timezone.now, verbose_name="Ngày giờ nhập")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name="Nhà cung cấp")
    license_plate = models.CharField(max_length=20, blank=True, null=True, verbose_name="Biển số xe")
    
    # File kết quả Spectro (PDF/Ảnh)
    spectro_file = models.FileField(
        upload_to='spectro_reports/%Y/%m/', 
        blank=True, 
        null=True, 
        verbose_name="Kết quả Spectro (PDF/Ảnh)"
    )
    
    note = models.TextField(blank=True, verbose_name="Ghi chú thêm")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.supplier.name}"

# 4. Chi tiết Phiếu Nhập (Detail) - Chứa từng mặt hàng cụ thể
# (LƯU Ý: Tên class ở đây phải là InputVoucherDetail)
class InputVoucherDetail(models.Model):
    voucher = models.ForeignKey(InputVoucher, related_name='details', on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialType, on_delete=models.PROTECT, verbose_name="Loại hàng")
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Khối lượng (kg)")
    price_per_kg = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Đơn giá / kg")
    
    # Tính thành tiền tạm tính (để hiển thị chơi, không lưu DB)
    @property
    def total_price(self):
        return self.quantity * self.price_per_kg

    def __str__(self):
        return f"{self.material_type.name} - {self.quantity}kg"