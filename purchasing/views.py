from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Supplier, PurchaseOrder, PurchaseInvoiceDetail
from .serializers import SupplierSerializer, PurchaseOrderSerializer, PurchaseInvoiceDetailSerializer
from users.permissions import IsAdmin
from purchasing.permissions import IsPurchasingOfficer, IsStoreKeeper

class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (IsPurchasingOfficer().has_permission(request, view) or 
                IsAdmin().has_permission(request, view))

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CustomPermission()]
        return [permissions.IsAuthenticated()]

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all().select_related('supplier', 'employee')
    serializer_class = PurchaseOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['supplier', 'status']
    ordering_fields = ['order_date', 'total_amount']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [permissions.IsAuthenticated(), CustomPermission()]
        elif self.action == 'receive':
            return [permissions.IsAuthenticated(), IsStoreKeeper()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'], permission_classes=[IsStoreKeeper])
    def receive(self, request, pk=None):
        order = self.get_object()
        if order.status == 'pending':
            order.status = 'received'
            order.save()
            return Response({'status': 'received'})
        return Response({'status': 'not allowed'}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)

class PurchaseInvoiceDetailViewSet(viewsets.ModelViewSet):
    queryset = PurchaseInvoiceDetail.objects.all().select_related('purchase_order', 'product')
    serializer_class = PurchaseInvoiceDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['purchase_order']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CustomPermission()]
        return [permissions.IsAuthenticated()]