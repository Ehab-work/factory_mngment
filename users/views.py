from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils import timezone
from .models import User, Notification
from .serializers import UserSerializer, NotificationSerializer
from .permissions import IsAdmin, IsUserOwner

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]
        elif self.action in ['retrieve', 'me']:
            return [permissions.IsAuthenticated(), IsUserOwner()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        if user.is_active:
            user.is_active = False
            user.save()
            Notification.objects.create(
                user=user,
                type='account_status',
                title='Account Deactivated',
                message='Your account has been deactivated by an admin.'
            )
            return Response({'status': 'deactivated'})
        return Response({'status': 'already deactivated'}, status=status.HTTP_400_BAD_REQUEST)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type', 'is_read']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        if notification.user == request.user and not notification.is_read:
            notification.is_read = True
            notification.save()
            return Response({'status': 'marked as read'})
        return Response({'status': 'not allowed'}, status=status.HTTP_400_BAD_REQUEST)