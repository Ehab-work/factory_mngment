from rest_framework import serializers
from .models import ProductionOrder, Task, ProductionConsumption

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.ReadOnlyField(source='assigned_to.username')
    
    class Meta:
        model = Task
        fields = '__all__'

class ProductionConsumptionSerializer(serializers.ModelSerializer):
    raw_material_name = serializers.ReadOnlyField(source='raw_material.name')
    
    class Meta:
        model = ProductionConsumption
        fields = '__all__'

class ProductionOrderSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    consumptions = ProductionConsumptionSerializer(many=True, read_only=True)
    product_name = serializers.ReadOnlyField(source='product.name')
    employee_name = serializers.ReadOnlyField(source='employee.username')
    
    class Meta:
        model = ProductionOrder
        fields = '__all__'