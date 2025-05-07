from rest_framework import serializers
from .models import ProductionOrder, ProductionTask, ProductionConsumption
from datetime import datetime

class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        if isinstance(value, datetime):
            return value.date()  # تحويل datetime إلى date
        return super().to_representation(value)

class ProductionOrderSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    employee_name = serializers.ReadOnlyField(source='employee.get_full_name')
    supervisor_name = serializers.ReadOnlyField(source='supervisor.get_full_name')
    start_date = CustomDateField(required=False)
    expected_end_date = serializers.DateField()

    class Meta:
        model = ProductionOrder
        fields = '__all__'
        read_only_fields = ['employee']

class ProductionTaskSerializer(serializers.ModelSerializer):
    production_order_id = serializers.ReadOnlyField(source='production_order.id')
    assigned_to_name = serializers.ReadOnlyField(source='assigned_to.get_full_name')
    assigned_by_name = serializers.ReadOnlyField(source='assigned_by.get_full_name')
    end_date = serializers.DateTimeField(required=False)

    class Meta:
        model = ProductionTask
        fields = '__all__'
        read_only_fields = ['assigned_by']

class ProductionConsumptionSerializer(serializers.ModelSerializer):
    production_order_id = serializers.ReadOnlyField(source='production_order.id')
    raw_material_name = serializers.ReadOnlyField(source='raw_material.name')
    recorded_by_name = serializers.ReadOnlyField(source='recorded_by.get_full_name')

    class Meta:
        model = ProductionConsumption
        fields = '__all__'
        read_only_fields = ['recorded_by', 'record_date']