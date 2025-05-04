from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RawMaterialViewSet, ProductViewSet, SupplierViewSet,
    InventoryMovementViewSet, RatioOfProductViewSet,
    MaterialRequestViewSet, UnitViewSet
)

router = DefaultRouter()
router.register(r'units', UnitViewSet)
router.register(r'raw-materials', RawMaterialViewSet)
router.register(r'products', ProductViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'inventory-movements', InventoryMovementViewSet)
router.register(r'ratios', RatioOfProductViewSet)
router.register(r'material-requests', MaterialRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
