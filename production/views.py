from rest_framework import viewsets
from .models import ProductionOrder, Task, ProductionConsumption
from .serializers import ProductionOrderSerializer, TaskSerializer, ProductionConsumptionSerializer
from users.permissions import IsWorker, IsProductionSupervisor, IsAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class ProductionOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductionOrder.objects.all()
    serializer_class = ProductionOrderSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsProductionSupervisor | IsAdmin]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsProductionSupervisor | IsAdmin]
        elif self.action == 'destroy':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'worker':
            # Workers can see production orders they're assigned to via tasks
            return ProductionOrder.objects.filter(tasks__assigned_to=user).distinct()
        elif user.role in ['production_supervisor', 'admin']:
            return ProductionOrder.objects.all()
        return ProductionOrder.objects.none()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsProductionSupervisor | IsAdmin]
        elif self.action in ['update', 'partial_update']:
            # Workers can only update status
            if self.request.user.role == 'worker':
                # Check implementation in perform_update
                permission_classes = [IsWorker | IsProductionSupervisor | IsAdmin]
            else:
                permission_classes = [IsProductionSupervisor | IsAdmin]
        elif self.action == 'destroy':
            permission_classes = [IsProductionSupervisor | IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'worker':
            return Task.objects.filter(assigned_to=user)
        elif user.role == 'production_supervisor':
            # Supervisors can see all tasks for the production orders they manage
            return Task.objects.filter(production_order__employee=user)
        elif user.role == 'admin':
            return Task.objects.all()
        return Task.objects.none()
    
    def perform_update(self, serializer):
        if self.request.user.role == 'worker':
            # Workers can only update the status field
            instance = self.get_object()
            if instance.assigned_to != self.request.user:
                raise PermissionDenied("You can only update tasks assigned to you")
            
            # Only allow updating status
            if set(self.request.data.keys()) - {'status'}:
                raise PermissionDenied("Workers can only update the status field")
            
            serializer.save()
        else:
            serializer.save()

class ProductionConsumptionViewSet(viewsets.ModelViewSet):
    queryset = ProductionConsumption.objects.all()
    serializer_class = ProductionConsumptionSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsProductionSupervisor | IsAdmin]
        elif self.action == 'destroy':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]