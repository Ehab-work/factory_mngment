from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProductionOrderViewSet, TaskViewSet, ProductionConsumptionViewSet

router = DefaultRouter()
router.register(r'production_orders', ProductionOrderViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'consumption', ProductionConsumptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
