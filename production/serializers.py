from rest_framework import serializers
from .models import FinishedBundle

class FinishedBundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishedBundle
        # Dưới đây là khai báo lấy tất cả các trường dữ liệu
        fields = '__all__' 
        # Hoặc nếu muốn chỉ định cụ thể: fields = ['id', 'barcode', 'weight', 'status']