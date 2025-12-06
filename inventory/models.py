from django.db import models

# 1. BẢNG KHÁCH HÀNG (Mới) 🤝
class Customer(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên công ty/Khách hàng")
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã KH")
    address = models.TextField(blank=True, verbose_name="Địa chỉ")
    
    def __str__(self):
        return f"{self.code} - {self.name}"

# 2. BẢNG LOẠI SẢN PHẨM (Giữ nguyên) 🧱
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên loại nhôm")
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã sản phẩm")
    description = models.TextField(blank=True, verbose_name="Mô tả/Tiêu chuẩn")

    def __str__(self):
        return f"{self.code} - {self.name}"

# 3. BẢNG MẺ NẤU / LOT NO (Cập nhật thêm Khách hàng) 🔥
class ProductionBatch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Loại sản phẩm")
    # Thêm liên kết với khách hàng (blank=True nghĩa là nấu để kho, chưa có khách cụ thể cũng được)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Dành cho KH")
    
    lot_no = models.CharField(max_length=50, unique=True, verbose_name="Mã Lot (LotNo)")
    production_date = models.DateField(verbose_name="Ngày sản xuất")
    
    # Những số liệu này sau này ta có thể tự động tính tổng từ bảng Package
    total_input_weight = models.FloatField(default=0, verbose_name="Tổng KL Nguyên liệu vào (kg)")
    
    # Các thông số kỹ thuật khác
    start_time = models.DateTimeField(null=True, blank=True, verbose_name="Bắt đầu nấu")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Kết thúc nấu")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")

    def __str__(self):
        return self.lot_no

# 4. BẢNG PHIẾU CÂN / KIỆN HÀNG (Mới tinh) ⚖️
class Package(models.Model):
    # Mỗi kiện hàng phải thuộc về một LotNo cụ thể
    batch = models.ForeignKey(ProductionBatch, on_delete=models.CASCADE, verbose_name="Thuộc Lot No")
    
    package_code = models.CharField(max_length=50, verbose_name="Mã kiện (VD: 01, 02...)")
    weight = models.FloatField(verbose_name="Khối lượng tịnh (Kg)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian cân")
    
    class Meta:
        verbose_name = "Phiếu cân / Kiện hàng"
        verbose_name_plural = "Danh sách Phiếu cân"
        # Đảm bảo trong 1 Lot không có 2 kiện cùng mã số
        unique_together = ('batch', 'package_code')

    def __str__(self):
        return f"Lot {self.batch.lot_no} - Kiện {self.package_code} ({self.weight}kg)"