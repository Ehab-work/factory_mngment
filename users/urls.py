from django.urls import path, include
from .views import (
    RegisterView, 
    MyTokenObtainPairView, 
    UserViewSet, 
    UserProfileView,
    UserLogoutView,
    ChangeUserRoleView,
    UserStatsView
)
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/<int:pk>/change-role/', ChangeUserRoleView.as_view(), name='change-user-role'),
    path('stats/', UserStatsView.as_view(), name='user-stats'),
    path('', include(router.urls)),
]