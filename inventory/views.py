from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Sum
from .models import Product, RawMaterial, RecipeOfProduct, InventoryMovement
from .serializers import ProductSerializer, RawMaterialSerializer, RecipeOfProductSerializer, InventoryMovementSerializer
from users.permissions import IsAdmin
from purchasing.permissions import IsStoreKeeper

class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (IsAdmin().has_permission(request, view) or 
                IsStoreKeeper().has_permission(request, view))

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'price', 'quantity']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CustomPermission()]
        return [permissions.IsAuthenticated()]

class RawMaterialViewSet(viewsets.ModelViewSet):
    queryset = RawMaterial.objects.all()
    serializer_class = RawMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'quantity', 'avg_price']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CustomPermission()]
        return [permissions.IsAuthenticated()]

class RecipeOfProductViewSet(viewsets.ModelViewSet):
    queryset = RecipeOfProduct.objects.all().select_related('product', 'raw_material')
    serializer_class = RecipeOfProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product', 'raw_material']
    search_fields = ['product__name', 'raw_material__name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]

class InventoryMovementViewSet(viewsets.ModelViewSet):
    queryset = InventoryMovement.objects.all().select_related('product', 'raw_material', 'moved_by')
    serializer_class = InventoryMovementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['move_type', 'reference_type']
    ordering_fields = ['move_date']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsStoreKeeper()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(moved_by=self.request.user)