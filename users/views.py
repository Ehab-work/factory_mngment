from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer, UserProfileSerializer, UserTokenSerializer,
    UserRoleSerializer, ChangePasswordSerializer, PublicUserSerializer
)
from .permissions import IsAdmin, IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from datetime import timedelta

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        if self.request.user.role == 'admin':
            return UserSerializer
        return PublicUserSerializer

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserLoginView(TokenObtainPairView):
    serializer_class = UserTokenSerializer

class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ChangeUserRoleView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == request.user:
            return Response({"detail": "لا يمكنك تغيير دورك الخاص."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self):
        return self.request.user

class UserStatsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        last_30_days = now() - timedelta(days=30)
        total_users = User.objects.count()
        active_recently = User.objects.filter(last_login__gte=last_30_days).count()
        return Response({
            "total_users": total_users,
            "active_last_30_days": active_recently
        })