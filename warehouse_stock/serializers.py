# warehouse_stock/serializers.py
from rest_framework import serializers
from django.utils import timezone
from django.db.models import Sum
from .models import InventoryItem, StockAdjustment

# Import Model từ App khác để tính toán (Import bên trong method để tránh lỗi vòng lặp)
# Lưu ý: Chúng ta sẽ import dynamic bên dưới

class InventoryItemSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material_type.name', read_only=True)
    material_code = serializers.CharField(source='material_type.code', read_only=True)
    unit = serializers.CharField(source='material_type.unit', read_only=True)
    
    # 2 trường tính toán mới
    planned_quantity = serializers.SerializerMethodField()
    pending_quantity = serializers.SerializerMethodField()

    class Meta:
        model = InventoryItem
        fields = ['id', 'material_type', 'material_name', 'material_code', 'quantity_on_hand', 'unit', 'last_updated', 'planned_quantity', 'pending_quantity']

    def get_planned_quantity(self, obj):
        """Lấy kế hoạch của tháng hiện tại"""
        from production.models import MonthlyPlan # Import ở đây để tránh Circular Import
        
        current_month = timezone.now().strftime('%Y-%m') # VD: "2024-01"
        plan = MonthlyPlan.objects.filter(material_type=obj.material_type, month=current_month).first()
        return plan.planned_quantity if plan else 0

    def get_pending_quantity(self, obj):
        """Tính tổng lượng hàng đã soạn (WAITING) đang nằm ở cửa lò"""
        from production.models import MaterialIssueDetail # Import ở đây
        
        # Lọc các phiếu cân trạng thái WAITING của loại vật tư này
        pending = MaterialIssueDetail.objects.filter(
            source_input__material_type=obj.material_type, 
            status='WAITING'
        ).aggregate(Sum('real_weight'))
        
        return pending['real_weight__sum'] or 0

class StockAdjustmentSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material_type.name', read_only=True)
    class Meta:
        model = StockAdjustment
        fields = '__all__'