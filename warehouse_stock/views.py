from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F

# Import các Models liên quan
from .models import InventoryItem, StockAdjustment
from .serializers import InventoryItemSerializer, StockAdjustmentSerializer
from warehouse_input.models import InputVoucherDetail
from production.models import FurnaceLog

class InventoryItemViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = InventoryItem.objects.all().order_by('material_type__name')
    serializer_class = InventoryItemSerializer

    # --- TÍNH NĂNG MỚI: LẤY LỊCH SỬ GIAO DỊCH ---
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """
        API này trả về lịch sử biến động của 1 vật tư.
        Logic: Gom tất cả Nhập + Xuất + Điều chỉnh -> Sắp xếp theo thời gian -> Tính tồn kho lũy kế.
        """
        inventory_item = self.get_object()
        material = inventory_item.material_type
        
        transactions = []

        # 1. Lấy lịch sử NHẬP KHO (+)
        inputs = InputVoucherDetail.objects.filter(material_type=material).select_related('voucher')
        for item in inputs:
            transactions.append({
                "date": item.voucher.date,
                "type": "NHAP",
                "quantity": item.quantity, # Số dương
                "reason": f"Phiếu nhập: {item.voucher.code}",
                "ref_id": item.voucher.id
            })

        # 2. Lấy lịch sử XUẤT SẢN XUẤT (NẤU LÒ) (-)
        outputs = FurnaceLog.objects.filter(material_type=material, action_type='ADD')
        for item in outputs:
            transactions.append({
                "date": item.timestamp,
                "type": "XUAT",
                "quantity": -item.quantity, # Số âm (trừ đi)
                "reason": f"Cấp lò: {item.batch.furnace_name} (Lot: {item.batch.lot_no})",
                "ref_id": item.batch.id
            })

        # 3. Lấy lịch sử KIỂM KÊ / ĐIỀU CHỈNH (+/-)
        adjusts = StockAdjustment.objects.filter(material_type=material)
        for item in adjusts:
            transactions.append({
                "date": item.date,
                "type": "DIEU_CHINH",
                "quantity": item.adjustment_quantity, # Có thể âm hoặc dương
                "reason": f"Kiểm kê: {item.code} ({item.reason})",
                "ref_id": item.id
            })

        # 4. Sắp xếp theo ngày tăng dần
        transactions.sort(key=lambda x: x['date'])

        # 5. Tính tồn kho lũy kế (Running Balance)
        running_balance = 0
        results = []
        for t in transactions:
            running_balance += float(t['quantity'])
            results.append({
                "date": t['date'],
                "reason": t['reason'],
                "change": t['quantity'],
                "balance": running_balance # Tồn cuối sau giao dịch này
            })

        # Đảo ngược lại để ngày mới nhất lên đầu cho dễ xem
        results.reverse()
        
        return Response(results)

class StockAdjustmentViewSet(viewsets.ModelViewSet):
    queryset = StockAdjustment.objects.all().order_by('-date')
    serializer_class = StockAdjustmentSerializer

def inventory_page(request):
    """Trả về giao diện báo cáo tồn kho"""
    return render(request, 'warehouse_stock/inventory.html')