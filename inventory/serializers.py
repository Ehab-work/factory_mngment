from rest_framework import serializers
from .models import RawMaterial, Product, InventoryMovement, RatioOfProduct, MaterialRequest

class RawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterial
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class InventoryMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMovement
        fields = '__all__'

class RatioOfProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatioOfProduct
        fields = '__all__'

class MaterialRequestSerializer(serializers.ModelSerializer):
    requested_by_name = serializers.ReadOnlyField(source='requested_by.username')
    raw_material_name = serializers.ReadOnlyField(source='raw_material.name')
    
    class Meta:
        model = MaterialRequest
        fields = '__all__'