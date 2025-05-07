from django.contrib import admin
from .models import ProductionOrder, ProductionTask, ProductionConsumption

@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'employee', 'status', 'start_date')
    list_filter = ('status', 'product')
    search_fields = ('product__name', 'notes')
    date_hierarchy = 'start_date'
    raw_id_fields = ('product', 'employee', 'supervisor')

@admin.register(ProductionTask)
class ProductionTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'production_order', 'status', 'assigned_to', 'start_date')
    list_filter = ('status', 'production_order')
    search_fields = ('name', 'description')
    date_hierarchy = 'start_date'
    raw_id_fields = ('production_order', 'assigned_to', 'assigned_by')

@admin.register(ProductionConsumption)
class ProductionConsumptionAdmin(admin.ModelAdmin):
    list_display = ('production_order', 'raw_material', 'quantity_used', 'record_date')
    list_filter = ('production_order',)
    search_fields = ('raw_material__name',)
    date_hierarchy = 'record_date'
    raw_id_fields = ('production_order', 'raw_material', 'recorded_by')