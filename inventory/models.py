from django.db import models

# 1. Bảng Loại Sản Phẩm (Ví dụ: ADC12, Nhôm thỏi 96%...)
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên loại nhôm")
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã sản phẩm")
    description = models.TextField(blank=True, verbose_name="Mô tả/Tiêu chuẩn")

    def __str__(self):
        return f"{self.code} - {self.name}"

# 2. Bảng Mẻ Nấu (Lot No) - Đây là trung tâm dữ liệu của bạn
class ProductionBatch(models.Model):
    # Liên kết: Một mẻ nấu phải thuộc về một loại sản phẩm nào đó
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Loại sản phẩm")
    
    # Thông tin định danh
    lot_no = models.CharField(max_length=50, unique=True, verbose_name="Mã Lot (LotNo)")
    production_date = models.DateField(verbose_name="Ngày sản xuất")
    
    # Số liệu sản xuất tổng quan
    total_input_weight = models.FloatField(default=0, verbose_name="Tổng KL Nguyên liệu vào (kg)")
    total_output_weight = models.FloatField(default=0, verbose_name="Tổng KL Thành phẩm ra (kg)")
    
    # Hiệu suất (Tính toán sau) và Thời gian
    start_time = models.DateTimeField(null=True, blank=True, verbose_name="Bắt đầu nấu")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Kết thúc nấu")
    
    # Ghi chú thêm
    notes = models.TextField(blank=True, verbose_name="Ghi chú")

    def __str__(self):
        return self.lot_no