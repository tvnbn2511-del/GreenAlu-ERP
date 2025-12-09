from django.apps import AppConfig


class WarehouseStockConfig(AppConfig):
    name = 'warehouse_stock'
def ready(self):
        import production.signals