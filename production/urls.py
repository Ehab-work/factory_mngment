from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductionOrderViewSet, ProductionTaskViewSet, ProductionConsumptionViewSet

router = DefaultRouter()
router.register(r'production-orders', ProductionOrderViewSet, basename='production-orders')
router.register(r'tasks', ProductionTaskViewSet, basename='tasks')
router.register(r'consumptions', ProductionConsumptionViewSet, basename='consumptions')

urlpatterns = [
    path('', include(router.urls)),
]