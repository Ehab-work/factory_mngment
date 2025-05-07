from django.contrib import admin
from .models import Client, SalesOrder, SalesInvoiceDetail

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')
    search_fields = ('name', 'email')
    ordering = ('name',)

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'employee', 'order_date', 'total_amount', 'status')
    list_filter = ('status', 'client')
    search_fields = ('client__name', 'notes')
    date_hierarchy = 'order_date'
    raw_id_fields = ('client', 'employee')

@admin.register(SalesInvoiceDetail)
class SalesInvoiceDetailAdmin(admin.ModelAdmin):
    list_display = ('sales_order', 'product', 'quantity', 'unit_price')
    list_filter = ('sales_order',)
    search_fields = ('product__name',)
    raw_id_fields = ('sales_order', 'product')