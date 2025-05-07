from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Sum
from .models import Client, SalesOrder, SalesInvoiceDetail
from .serializers import ClientSerializer, SalesOrderSerializer, SalesInvoiceDetailSerializer
from .permissions import IsSalesRep, IsSalesSupervisor
from users.permissions import IsAdmin
from inventory.models import Product, InventoryMovement
from users.models import Notification

class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (IsSalesRep().has_permission(request, view) or 
                IsSalesSupervisor().has_permission(request, view) or 
                IsAdmin().has_permission(request, view))

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CustomPermission()]
        return [permissions.IsAuthenticated()]

class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all().select_related('client', 'employee').prefetch_related('sales_invoice_details')
    serializer_class = SalesOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['client', 'status']
    ordering_fields = ['order_date', 'total_amount']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [permissions.IsAuthenticated(), CustomPermission()]
        elif self.action in ['destroy', 'confirm', 'ship', 'cancel']:
            return [permissions.IsAuthenticated(), IsSalesSupervisor() | IsAdmin()]  # يمكن نعدله لـ CustomPermission لاحقًا
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsSalesSupervisor])
    def confirm(self, request, pk=None):
        order = self.get_object()
        if order.status == 'pending':
            order.status = 'confirmed'
            order.save()
            Notification.objects.create(
                user=order.employee,
                type='order_status',
                title='Sales Order Confirmed',
                message=f'Sales Order #{order.id} has been confirmed by {request.user.get_full_name()}.',
                reference_id=order.id,
                reference_type='SalesOrder'
            )
            return Response({'status': 'confirmed'})
        return Response({'status': 'not allowed'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsSalesSupervisor])
    def ship(self, request, pk=None):
        order = self.get_object()
        if order.status == 'confirmed':
            order.status = 'shipped'
            order.save()
            for detail in order.sales_invoice_details.all():
                product = detail.product
                product.quantity -= detail.quantity
                product.save()
                InventoryMovement.objects.create(
                    product=product,
                    quantity=detail.quantity,
                    move_type='out',
                    moved_by=self.request.user,
                    reference_type='sales',
                    reference_id=order.id,
                    notes=f'Shipped for Sales Order #{order.id}'
                )
            Notification.objects.create(
                user=order.employee,
                type='order_status',
                title='Sales Order Shipped',
                message=f'Sales Order #{order.id} has been shipped by {request.user.get_full_name()}.',
                reference_id=order.id,
                reference_type='SalesOrder'
            )
            return Response({'status': 'shipped'})
        return Response({'status': 'not allowed'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsSalesSupervisor])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status in ['pending', 'confirmed']:
            order.status = 'cancelled'
            order.save()
            Notification.objects.create(
                user=order.employee,
                type='order_status',
                title='Sales Order Cancelled',
                message=f'Sales Order #{order.id} has been cancelled by {request.user.get_full_name()}.',
                reference_id=order.id,
                reference_type='SalesOrder'
            )
            return Response({'status': 'cancelled'})
        return Response({'status': 'not allowed'}, status=status.HTTP_400_BAD_REQUEST)

class SalesInvoiceDetailViewSet(viewsets.ModelViewSet):
    queryset = SalesInvoiceDetail.objects.all().select_related('sales_order', 'product')
    serializer_class = SalesInvoiceDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sales_order']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CustomPermission()]
        return [permissions.IsAuthenticated()]