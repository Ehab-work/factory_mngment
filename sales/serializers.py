from rest_framework import serializers
from .models import Client, SalesOrder, SalesInvoiceDetail

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class SalesOrderSerializer(serializers.ModelSerializer):
    client_name = serializers.ReadOnlyField(source='client.name')
    employee_name = serializers.ReadOnlyField(source='employee.get_full_name')
    details = serializers.SerializerMethodField()
    order_date = serializers.DateTimeField(required=False)

    class Meta:
        model = SalesOrder
        fields = '__all__'
        read_only_fields = ['employee']

    def get_details(self, obj):
        details = obj.sales_invoice_details.all()
        return SalesInvoiceDetailSerializer(details, many=True).data

class SalesInvoiceDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = SalesInvoiceDetail
        fields = '__all__'