from django.contrib import admin
from .models import Client, SalesOrder, SalesInvoiceDetail

class SalesInvoiceDetailInline(admin.TabularInline):
    model = SalesInvoiceDetail
    extra = 1

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'employee', 'sale_date', 'total_amount', 'status')
    list_filter = ('status', 'sale_date')
    search_fields = ('client__name', 'employee__username')
    inlines = [SalesInvoiceDetailInline]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    search_fields = ('name', 'email')

admin.site.register(SalesInvoiceDetail)
