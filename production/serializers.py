from rest_framework import serializers
from .models import FinishedBundle, Customer, ProductionBatch

# 1. Serializer cho Kiện hàng
class FinishedBundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishedBundle
        fields = '__all__'

# 2. Serializer cho Khách hàng (Sửa lại chỗ này)
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:  # <--- Dòng này phải thụt vào (bấm Tab 1 lần)
        model = Customer
        fields = '__all__'

# 3. Serializer cho Mẻ nấu (Sửa lại chỗ này)
class ProductionBatchSerializer(serializers.ModelSerializer):
    class Meta:  # <--- Dòng này cũng phải thụt vào
        model = ProductionBatch
        fields = '__all__'