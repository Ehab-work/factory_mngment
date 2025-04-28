from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RawMaterial, Product, InventoryMovement, RatioOfProduct, MaterialRequest
from .serializers import RawMaterialSerializer, ProductSerializer, InventoryMovementSerializer, RatioOfProductSerializer, MaterialRequestSerializer
from users.permissions import IsStoreKeeper, IsAdmin, IsWorker, IsProductionSupervisor
from rest_framework.permissions import IsAuthenticated

class RawMaterialViewSet(viewsets.ModelViewSet):
    queryset = RawMaterial.objects.all()
    serializer_class = RawMaterialSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsStoreKeeper | IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsStoreKeeper | IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class InventoryMovementViewSet(viewsets.ModelViewSet):
    queryset = InventoryMovement.objects.all()
    serializer_class = InventoryMovementSerializer
    
    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsStoreKeeper | IsAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class RatioOfProductViewSet(viewsets.ModelViewSet):
    queryset = RatioOfProduct.objects.all()
    serializer_class = RatioOfProductSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class MaterialRequestViewSet(viewsets.ModelViewSet):
    queryset = MaterialRequest.objects.all()
    serializer_class = MaterialRequestSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsWorker | IsProductionSupervisor | IsAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)
        
    @action(detail=True, methods=['post'], permission_classes=[IsStoreKeeper | IsAdmin])
    def approve(self, request, pk=None):
        material_request = self.get_object()
        material_request.status = 'approved'
        material_request.approved_by = request.user
        material_request.save()
        return Response({'status': 'request approved'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsStoreKeeper | IsAdmin])
    def reject(self, request, pk=None):
        material_request = self.get_object()
        material_request.status = 'rejected'
        material_request.approved_by = request.user
        material_request.save()
        return Response({'status': 'request rejected'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsStoreKeeper | IsAdmin])
    def complete(self, request, pk=None):
        material_request = self.get_object()
        
        # Make sure the request is approved
        if material_request.status != 'approved':
            return Response(
                {'error': 'Cannot complete a request that is not approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the raw material and check availability
        raw_material = material_request.raw_material
        if raw_material.quantity < material_request.quantity:
            return Response(
                {'error': 'Insufficient quantity available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update inventory
        raw_material.quantity -= material_request.quantity
        raw_material.save()
        
        # Record inventory movement
        InventoryMovement.objects.create(
            material_type='raw',
            material_id=raw_material.id,
            quantity=material_request.quantity,
            movement_type='OUT',
            note=f"Issued for material request #{material_request.id}",
            created_by=request.user
        )
        
        # Update the material request
        material_request.status = 'completed'
        material_request.save()
        
        return Response({'status': 'request completed'})