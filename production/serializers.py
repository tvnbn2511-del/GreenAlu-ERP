# production/serializers.py
from rest_framework import serializers
from .models import FinishedBundle, Customer, ProductionBatch, WeighingSlip
from django.db.models import Sum

# ---------------------------------------------------------
# 1. Serializer cho Kiện hàng (Chỉ hiển thị thông tin kiện)
# ---------------------------------------------------------
class FinishedBundleSerializer(serializers.ModelSerializer):
    # 1. Lấy mã mẻ (Bạn đã có cái này rồi)
    batch_code = serializers.CharField(source='batch.lot_no', read_only=True)
    
    # 2. Lấy tên khách hàng (Để hiển thị trên bảng kiện)
    customer_name = serializers.CharField(
        source='batch.target_standard.customer.name', 
        read_only=True, 
        default="-"
        )
    
    # 3. Lấy loại nhôm
    alloy = serializers.CharField(
        source='batch.target_standard.alloy_type', 
        read_only=True, 
        default="-"
    )
    class Meta:
        model = FinishedBundle
        fields = '__all__'

# ---------------------------------------------------------
# 2. Serializer cho Mẻ nấu (Chứa logic tính tổng trọng lượng)
# ---------------------------------------------------------
class ProductionBatchSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source='target_standard.customer.name', 
        read_only=True, 
        default="-"
    )
    
    alloy_name = serializers.CharField(
        source='target_standard.alloy_type', 
        read_only=True, 
        default="-"
    )

    total_weight = serializers.SerializerMethodField()
    total_bundles = serializers.SerializerMethodField()

    class Meta:
        model = ProductionBatch
        fields = [
            'id', 
            'lot_no',       # Sửa 'code' thành 'lot_no' (Theo log lỗi của bạn)
            'date_started', # Sửa 'date' thành 'date_started' (Theo log lỗi của bạn)
            'customer_name', 
            'alloy_name',
            'total_weight', 
            'total_bundles'
        ]

    def get_total_weight(self, obj):
        # QUAN TRỌNG: Kiểm tra related_name trong models.py
        # Nếu model FinishedBundle dòng 'batch' bạn KHÔNG ghi related_name='bundles'
        # Thì mặc định Django dùng tên: 'finishedbundle_set' (như trong log lỗi gợi ý)
        
        # Hãy thử dùng 'finishedbundle_set' nếu 'bundles' báo lỗi
        bundles = getattr(obj, 'bundles', None) or getattr(obj, 'finishedbundle_set', None)
        
        if bundles:
            result = bundles.aggregate(Sum('weight'))
            return result['weight__sum'] or 0
        return 0

    def get_total_bundles(self, obj):
        bundles = getattr(obj, 'bundles', None) or getattr(obj, 'finishedbundle_set', None)
        if bundles:
            return bundles.count()
        return 0

# ---------------------------------------------------------
# 3. Các Serializer khác
# ---------------------------------------------------------
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class WeighingSlipSerializer(serializers.ModelSerializer):
    total_bundles = serializers.SerializerMethodField()
    total_weight = serializers.SerializerMethodField()

    class Meta:
        model = WeighingSlip
        fields = '__all__'
        extra_kwargs = {
            'note': {'required': False, 'allow_blank': True}
        }

    def get_total_bundles(self, obj):
        # Tương tự, kiểm tra related_name trong model WeighingSlip
        items = getattr(obj, 'bundles', None) or getattr(obj, 'finishedbundle_set', None)
        return items.count() if items else 0

    def get_total_weight(self, obj):
        items = getattr(obj, 'bundles', None) or getattr(obj, 'finishedbundle_set', None)
        if items:
            result = items.aggregate(Sum('weight'))
            return result['weight__sum'] or 0
        return 0