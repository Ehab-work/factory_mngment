from rest_framework import serializers
from .models import Client, SalesOrder, SalesInvoiceDetail

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class SalesInvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInvoiceDetail
        fields = '__all__'

class SalesOrderSerializer(serializers.ModelSerializer):
    details = SalesInvoiceDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = SalesOrder
        fields = '__all__'
        read_only_fields = ['employee', 'sale_date']
    
    def create(self, validated_data):
        sale = SalesOrder.objects.create(**validated_data)
        details_data = self.context['request'].data.get('details', [])
        
        for detail_data in details_data:
            SalesInvoiceDetail.objects.create(sale=sale, **detail_data)
        
        return sale