from rest_framework import serializers
from .models import Supplier, PurchaseOrder, PurchaseInvoiceDetail

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier_name = serializers.ReadOnlyField(source='supplier.name')
    employee_name = serializers.ReadOnlyField(source='employee.get_full_name')
    details = serializers.SerializerMethodField()
    order_date = serializers.DateTimeField(required=False)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only_fields = ['employee']

    def get_details(self, obj):
        details = obj.purchase_invoice_details.all()
        return PurchaseInvoiceDetailSerializer(details, many=True).data

class PurchaseInvoiceDetailSerializer(serializers.ModelSerializer):
    raw_material_name = serializers.ReadOnlyField(source='raw_material.name')

    class Meta:
        model = PurchaseInvoiceDetail
        fields = '__all__'