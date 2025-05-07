from django.contrib import admin
from .models import Product, RawMaterial, RecipeOfProduct, InventoryMovement

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'avg_price')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(RecipeOfProduct)
class RecipeOfProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'raw_material', 'quantity')
    list_filter = ('product', 'raw_material')
    search_fields = ('product__name', 'raw_material__name')
    raw_id_fields = ('product', 'raw_material')

@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ('move_type', 'product', 'raw_material', 'quantity', 'move_date', 'moved_by')
    list_filter = ('move_type', 'reference_type')
    search_fields = ('product__name', 'raw_material__name', 'notes')
    date_hierarchy = 'move_date'
    raw_id_fields = ('product', 'raw_material', 'moved_by')