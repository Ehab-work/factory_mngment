from django.contrib import admin
from .models import Supplier, PurchaseOrder, PurchaseInvoiceDetail

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email')
    search_fields = ('name', 'email')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'employee', 'order_date', 'total_amount', 'status')
    list_filter = ('status', 'supplier')
    search_fields = ('supplier__name', 'notes')
    date_hierarchy = 'order_date'
    raw_id_fields = ('supplier', 'employee')

@admin.register(PurchaseInvoiceDetail)
class PurchaseInvoiceDetailAdmin(admin.ModelAdmin):
    list_display = ('purchase_order', 'raw_material', 'quantity', 'unit_price')
    list_filter = ('purchase_order',)
    search_fields = ('raw_material__name',)
    raw_id_fields = ('purchase_order', 'raw_material')