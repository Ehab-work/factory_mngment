from rest_framework import serializers
from .models import Client, SalesOrder, SalesInvoiceDetail
from inventory.serializers import ProductSerializer
from users.serializers import UserSerializer

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class SalesInvoiceDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=SalesInvoiceDetail._meta.get_field('product').related_model.objects.all(), source='product', write_only=True)

    class Meta:
        model = SalesInvoiceDetail
        fields = ['id', 'sale', 'product', 'product_id', 'quantity', 'unit_price']

class SalesOrderSerializer(serializers.ModelSerializer):
    employee = UserSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(queryset=SalesOrder._meta.get_field('employee').related_model.objects.all(), source='employee', write_only=True)
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(queryset=SalesOrder._meta.get_field('client').related_model.objects.all(), source='client', write_only=True)
    details = SalesInvoiceDetailSerializer(many=True, read_only=True)

    class Meta:
        model = SalesOrder
        fields = ['id', 'employee', 'employee_id', 'client', 'client_id', 'sale_date', 'discount', 'total_amount', 'status', 'details']