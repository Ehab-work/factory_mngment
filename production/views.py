from rest_framework import viewsets, permissions
from .models import ProductionOrder, Task
from .serializers import ProductionOrderSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsWorker, IsSupervisor, IsAdmin

class ProductionOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductionOrder.objects.all()
    serializer_class = ProductionOrderSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdmin() | IsSupervisor()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'worker':
            return ProductionOrder.objects.filter(tasks__assigned_to=user).distinct()
        elif user.role == 'supervisor':
            return ProductionOrder.objects.filter(supervisor=user)
        return ProductionOrder.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('assigned_to', 'order').all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsAdmin() | IsSupervisor()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'worker':
            return Task.objects.filter(assigned_to=user)
        elif user.role == 'supervisor':
            return Task.objects.filter(order__supervisor=user)
        return Task.objects.all()

    def perform_update(self, serializer):
        user = self.request.user
        if user.role == 'worker':
            # العامل لا يُسمح له إلا بتحديث الحالة فقط
            serializer.save(status=serializer.validated_data.get('status', None))
        else:
            serializer.save()