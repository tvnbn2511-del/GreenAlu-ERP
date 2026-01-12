from rest_framework import serializers
from .models import (
    ProductionOrder, ProductionOrderItem, MaterialIssueDetail,
    ProductionBatch, FurnaceLog, WeighingSlip, FinishedBundle,
    Customer, ProductStandard, AlloyType
)

# ==========================================================
# 1. CÁC SERIALIZERS PHỤ (Define trước để dùng sau)
# ==========================================================

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class AlloyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlloyType
        fields = '__all__'

class ProductStandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStandard
        fields = '__all__'

# ==========================================================
# 2. CHI TIẾT LỆNH (PHẢI ĐẶT TRÊN 'PRODUCTION ORDER')
# ==========================================================

class ProductionOrderItemSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material_type.name', read_only=True)
    
    class Meta:
        model = ProductionOrderItem
        fields = ['id', 'material_type', 'material_name', 'quantity_required']

# ==========================================================
# 3. LỆNH SẢN XUẤT (GỌI ĐẾN CHI TIẾT LỆNH)
# ==========================================================

class ProductionOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    product_type_name = serializers.CharField(source='product_type.name', read_only=True)
    
    # Lúc này Python đã biết ProductionOrderItemSerializer là ai rồi
    items = ProductionOrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProductionOrder
        fields = ['id', 'lot_no', 'customer', 'customer_name', 
                  'product_type', 'product_type_name', 
                  'target_quantity', 'status', 'date_created', 'note', 'items']

# ==========================================================
# 4. KHO: PHIẾU SOẠN HÀNG
# ==========================================================

class MaterialIssueDetailSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='source_input.material_type.name', read_only=True)
    lot_input = serializers.CharField(source='source_input.supplier_lot_no', read_only=True)
    
    class Meta:
        model = MaterialIssueDetail
        fields = ['id', 'production_order', 'source_input', 'material_name', 'lot_input', 'real_weight', 'status']

# ==========================================================
# 5. LÒ: NHẬT KÝ & MẺ NẤU
# ==========================================================

class FurnaceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FurnaceLog
        fields = '__all__'

class ProductionBatchSerializer(serializers.ModelSerializer):
    lot_no = serializers.CharField(source='production_order.lot_no', read_only=True)
    
    class Meta:
        model = ProductionBatch
        fields = ['id', 'production_order', 'lot_no', 'furnace_name', 
                  'start_time', 'end_time', 'status', 'si_final', 'fe_final', 'cu_final']

# ==========================================================
# 6. THÀNH PHẨM
# ==========================================================

class FinishedBundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishedBundle
        fields = '__all__'

class WeighingSlipSerializer(serializers.ModelSerializer):
    lot_no = serializers.CharField(source='production_order.lot_no', read_only=True)
    bundles = FinishedBundleSerializer(many=True, read_only=True)
    
    class Meta:
        model = WeighingSlip
        fields = ['id', 'code', 'production_order', 'lot_no', 'date', 'bundles']