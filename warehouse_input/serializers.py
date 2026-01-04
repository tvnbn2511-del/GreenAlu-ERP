from rest_framework import serializers
from .models import MaterialType, Supplier, InputVoucher, InputVoucherDetail

# 1. Serializer cho Vật tư & NCC (Đơn giản)
class MaterialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialType
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

# 2. Serializer cho Chi tiết phiếu nhập
class InputVoucherDetailSerializer(serializers.ModelSerializer):
    # Hiển thị thêm tên vật tư để dễ nhìn trên Frontend
    material_name = serializers.CharField(source='material_type.name', read_only=True)
    material_code = serializers.CharField(source='material_type.code', read_only=True)
    
    total_price = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model = InputVoucherDetail
        fields = ['id', 'material_type', 'material_name', 'material_code', 
                  'supplier_lot_no', 'quantity', 'unit_price', 'total_price',
                  'si_test', 'fe_test', 'cu_test']

# 3. Serializer cho Phiếu nhập (QUAN TRỌNG)
class InputVoucherSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    details = InputVoucherDetailSerializer(many=True) # Cho phép gửi kèm danh sách chi tiết
    total_amount = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model = InputVoucher
        fields = ['id', 'code', 'date', 'supplier', 'supplier_name', 'note', 'details', 'total_amount']

    # Hàm này xử lý việc lưu cùng lúc Phiếu + Chi tiết
    def create(self, validated_data):
        details_data = validated_data.pop('details') # Tách phần chi tiết ra
        voucher = InputVoucher.objects.create(**validated_data) # Tạo phiếu trước
        
        # Sau đó tạo từng dòng chi tiết gắn vào phiếu
        for detail_data in details_data:
            InputVoucherDetail.objects.create(voucher=voucher, **detail_data)
        
        return voucher