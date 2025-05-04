from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Supplier, PurchaseOrder, PurchaseInvoiceDetail
from .serializers import SupplierSerializer, PurchaseOrderSerializer, PurchaseInvoiceDetailSerializer
from users.permissions import IsAdmin, IsStoreKeeper
from rest_framework.permissions import IsAuthenticated
from inventory.models import RawMaterial, InventoryMovement
from datetime import datetime

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdmin()]
        elif self.action in ['approve_order', 'reject_order', 'receive_materials']:
            return [IsAuthenticated(), IsStoreKeeper()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def approve_order(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response({"detail": "لا يمكن اعتماد أمر تم معالجته بالفعل."}, status=400)
        order.status = 'approved'
        order.approved_date = datetime.now()
        order.save()
        return Response({"detail": "تم اعتماد أمر الشراء."})

    @action(detail=True, methods=['post'])
    def reject_order(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response({"detail": "لا يمكن رفض أمر تم معالجته بالفعل."}, status=400)
        order.status = 'rejected'
        order.save()
        return Response({"detail": "تم رفض أمر الشراء."})

    @action(detail=True, methods=['post'])
    def receive_materials(self, request, pk=None):
        order = self.get_object()
        if order.status != 'approved':
            return Response({"detail": "لا يمكن استلام المواد قبل اعتماد الطلب."}, status=400)

        details = PurchaseInvoiceDetail.objects.filter(purchase_order=order)
        for detail in details:
            material = detail.material
            material.quantity_in_stock += detail.quantity
            material.price_per_unit = detail.unit_price  # اختيارياً تحدّث السعر
            material.save()

            InventoryMovement.objects.create(
                material=material,
                movement_type='in',
                quantity=detail.quantity,
                related_order=order
            )

        order.status = 'received'
        order.received_date = datetime.now()
        order.save()
        return Response({"detail": "تم استلام المواد وتحديث المخزون."})

class PurchaseInvoiceDetailViewSet(viewsets.ModelViewSet):
    queryset = PurchaseInvoiceDetail.objects.all()
    serializer_class = PurchaseInvoiceDetailSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
