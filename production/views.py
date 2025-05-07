from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Sum
from .models import ProductionOrder, ProductionTask, ProductionConsumption
from .serializers import ProductionOrderSerializer, ProductionTaskSerializer, ProductionConsumptionSerializer
from users.permissions import IsAdmin
from production.permissions import IsProductionSupervisor, IsWorker

class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (IsAdmin().has_permission(request, view) or 
                IsProductionSupervisor().has_permission(request, view))

class ProductionOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductionOrder.objects.all().select_related('product')
    serializer_class = ProductionOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['order_date', 'estimated_completion_date']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CustomPermission()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)

class ProductionTaskViewSet(viewsets.ModelViewSet):
    queryset = ProductionTask.objects.all().select_related('production_order', 'assigned_to')
    serializer_class = ProductionTaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'production_order']
    ordering_fields = ['due_date']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CustomPermission()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

class ProductionConsumptionViewSet(viewsets.ModelViewSet):
    queryset = ProductionConsumption.objects.all().select_related('production_task', 'raw_material')
    serializer_class = ProductionConsumptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['production_task']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsWorker() | IsProductionSupervisor()]  # يمكن نعدله لـ CustomPermission لاحقًا
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)