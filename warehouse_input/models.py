from django.db import models
from django.utils import timezone

class MaterialType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên loại vật tư")
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã VT")
    unit = models.CharField(max_length=20, default="kg", verbose_name="Đơn vị")
    def __str__(self): return f"{self.name} ({self.code})"

class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nhà cung cấp")
    def __str__(self): return self.name

class InputVoucher(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã phiếu nhập")
    date = models.DateTimeField(default=timezone.now, verbose_name="Ngày nhập")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name="Nhà cung cấp")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.code

class InputVoucherDetail(models.Model):
    voucher = models.ForeignKey(InputVoucher, related_name='details', on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialType, on_delete=models.PROTECT, verbose_name="Loại hàng")
    quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Khối lượng (kg)")
    
    # Kết quả test mẫu đầu vào (QC Input)
    si_test = models.FloatField(default=0, verbose_name="Si (%)")
    fe_test = models.FloatField(default=0, verbose_name="Fe (%)")
    cu_test = models.FloatField(default=0, verbose_name="Cu (%)")

    def __str__(self): return f"{self.material_type.name} - {self.quantity}kg"