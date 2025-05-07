from rest_framework import serializers
from .models import Product, RawMaterial, RecipeOfProduct, InventoryMovement

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class RawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterial
        fields = '__all__'

class RecipeOfProductSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    raw_material_name = serializers.ReadOnlyField(source='raw_material.name')

    class Meta:
        model = RecipeOfProduct
        fields = '__all__'

class InventoryMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    raw_material_name = serializers.ReadOnlyField(source='raw_material.name')
    moved_by_name = serializers.ReadOnlyField(source='moved_by.get_full_name')

    class Meta:
        model = InventoryMovement
        fields = '__all__'
        read_only_fields = ['moved_by', 'move_date']