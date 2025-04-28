from rest_framework import serializers
from .models import Supplier, PurchaseOrder, PurchaseInvoiceDetail

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class PurchaseInvoiceDetailSerializer(serializers.ModelSerializer):
    raw_material_name = serializers.ReadOnlyField(source='raw_material.name')
    
    class Meta:
        model = PurchaseInvoiceDetail
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    details = PurchaseInvoiceDetailSerializer(many=True, read_only=True)
    employee_name = serializers.ReadOnlyField(source='employee.username')
    supplier_name = serializers.ReadOnlyField(source='supplier.name')
    
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only_fields = ['employee']
    
    def create(self, validated_data):
        order = PurchaseOrder.objects.create(**validated_data)
        details_data = self.context['request'].data.get('details', [])
        
        for detail_data in details_data:
            PurchaseInvoiceDetail.objects.create(order=order, **detail_data)
        
        return order