from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Supplier, PurchaseOrder, PurchaseInvoiceDetail
from .serializers import SupplierSerializer, PurchaseOrderSerializer, PurchaseInvoiceDetailSerializer
from users.permissions import IsPurchasingOfficer, IsAdmin, IsStoreKeeper
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from inventory.models import RawMaterial, InventoryMovement

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsPurchasingOfficer | IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsPurchasingOfficer | IsAdmin]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAdmin]
        elif self.action == 'destroy':
            permission_classes = [IsAdmin]
        elif self.action in ['approve', 'reject']:
            permission_classes = [IsAdmin]
        elif self.action == 'receive_materials':
            permission_classes = [IsStoreKeeper | IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        if not (self.request.user.role == 'purchasing_officer' or self.request.user.role == 'admin'):
            raise PermissionDenied("Only purchasing officers can create orders")
        serializer.save(employee=self.request.user)
    
    def perform_update(self, serializer):
        if not self.request.user.role == 'admin':
            raise PermissionDenied("Only admin can update orders")
        serializer.save()
        
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.status = 'approved'
        purchase_order.save()
        return Response({'status': 'purchase order approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.status = 'rejected'
        purchase_order.save()
        return Response({'status': 'purchase order rejected'})
    
    @action(detail=True, methods=['post'])
    def receive_materials(self, request, pk=None):
        purchase_order = self.get_object()
        
        if purchase_order.status != 'approved':
            return Response(
                {'error': 'Cannot receive materials for an order that is not approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        for detail in purchase_order.details.all():
            raw_material = detail.raw_material
            
            # Update material quantity
            old_quantity = raw_material.quantity
            old_avg_price = raw_material.avg_price
            
            # Calculate new average price
            new_total_value = (old_quantity * old_avg_price) + (detail.quantity * detail.unit_price)
            new_total_quantity = old_quantity + detail.quantity
            new_avg_price = new_total_value / new_total_quantity if new_total_quantity > 0 else detail.unit_price
            
            # Update raw material
            raw_material.quantity = new_total_quantity
            raw_material.avg_price = new_avg_price
            raw_material.save()
            
            # Record inventory movement
            InventoryMovement.objects.create(
                material_type='raw',
                material_id=raw_material.id,
                quantity=detail.quantity,
                movement_type='IN',
                note=f"Received from purchase order #{purchase_order.id}",
                created_by=request.user
            )
        
        # Update purchase order
        purchase_order.status = 'completed'
        purchase_order.save()
        
        return Response({'status': 'materials received successfully'})

class PurchaseInvoiceDetailViewSet(viewsets.ModelViewSet):
    queryset = PurchaseInvoiceDetail.objects.all()
    serializer_class = PurchaseInvoiceDetailSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsPurchasingOfficer | IsAdmin]
        elif self.action == 'destroy':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]