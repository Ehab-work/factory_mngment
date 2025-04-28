from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RawMaterialViewSet, ProductViewSet, InventoryMovementViewSet, RatioOfProductViewSet, MaterialRequestViewSet

router = DefaultRouter()
router.register(r'raw-materials', RawMaterialViewSet)
router.register(r'products', ProductViewSet)
router.register(r'movements', InventoryMovementViewSet)
router.register(r'product-ratios', RatioOfProductViewSet)
router.register(r'material-requests', MaterialRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]