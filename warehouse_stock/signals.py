from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StockAdjustment, InventoryItem

@receiver(post_save, sender=StockAdjustment)
def adjust_inventory(sender, instance, created, **kwargs):
    if created:
        item, _ = InventoryItem.objects.get_or_create(material_type=instance.material_type)
        item.quantity_on_hand += instance.adjustment_quantity
        item.save()