from rest_framework import viewsets
from .models import Client, SalesOrder, SalesInvoiceDetail
from .serializers import ClientSerializer, SalesOrderSerializer, SalesInvoiceDetailSerializer
from users.permissions import IsSalesRep, IsSalesSupervisor, IsAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsSalesRep | IsSalesSupervisor | IsAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsSalesRep | IsAdmin]
        elif self.action == 'destroy':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'sales_rep':
            return SalesOrder.objects.filter(employee=user)
        elif user.role == 'sales_supervisor':
            # Assuming sales reps are assigned to supervisors somehow
            # This is a simplified example
            return SalesOrder.objects.filter(employee__role='sales_rep')
        elif user.role in ['admin']:
            return SalesOrder.objects.all()
        return SalesOrder.objects.none()
    
    def perform_create(self, serializer):
        if not (self.request.user.role == 'sales_rep' or self.request.user.role == 'admin'):
            raise PermissionDenied("Only sales representatives can create sales")
        serializer.save(employee=self.request.user)
    
    def perform_update(self, serializer):
        raise PermissionDenied("Updating sales is not allowed")
    
    def perform_destroy(self, instance):
        if not self.request.user.role == 'admin':
            raise PermissionDenied("Only admins can delete sales")
        instance.delete()

class SalesInvoiceDetailViewSet(viewsets.ModelViewSet):
    queryset = SalesInvoiceDetail.objects.all()
    serializer_class = SalesInvoiceDetailSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsSalesRep | IsAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]