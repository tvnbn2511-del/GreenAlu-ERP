from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
# Dòng quan trọng: Phải import đủ DeliveryNote và FinishedBundle
from .models import FurnaceLog, ScrapReturn, DeliveryNote, FinishedBundle 
from warehouse_stock.models import InventoryItem
from warehouse_input.models import InputVoucherDetail
from decimal import Decimal

# 1. Nhập kho -> Cộng tồn
@receiver(post_save, sender=InputVoucherDetail)
def stock_in(sender, instance, created, **kwargs):
    if created:
        item, _ = InventoryItem.objects.get_or_create(material_type=instance.material_type)
        item.quantity_on_hand += instance.quantity
        item.save()

# 2. Nạp lò -> Trừ tồn
@receiver(post_save, sender=FurnaceLog)
def stock_out_furnace(sender, instance, created, **kwargs):
    if created and instance.action_type == 'ADD' and instance.material_type:
        item, _ = InventoryItem.objects.get_or_create(material_type=instance.material_type)
        item.quantity_on_hand -= Decimal(instance.quantity)
        item.save()

# 3. Hàng lỗi quay đầu -> Cộng tồn
@receiver(post_save, sender=ScrapReturn)
def stock_return_scrap(sender, instance, created, **kwargs):
    if created:
        item, _ = InventoryItem.objects.get_or_create(material_type=instance.material_type)
        item.quantity_on_hand += instance.quantity
        item.save()

# 4. XUẤT HÀNG -> ĐỔI TRẠNG THÁI KIỆN (Mới -> Đã bán)
@receiver(m2m_changed, sender=DeliveryNote.bundles.through)
def update_bundle_status_on_delivery(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        # Khi add kiện vào phiếu xuất -> Đổi status thành SOLD
        FinishedBundle.objects.filter(pk__in=pk_set).update(status='SOLD')
    elif action == "post_remove":
        # Nếu lỡ tay xóa khỏi phiếu xuất -> Trả lại status NEW
        FinishedBundle.objects.filter(pk__in=pk_set).update(status='NEW')