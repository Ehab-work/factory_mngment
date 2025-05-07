from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, RawMaterialViewSet, RecipeOfProductViewSet, InventoryMovementViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'raw-materials', RawMaterialViewSet, basename='raw-materials')
router.register(r'recipes', RecipeOfProductViewSet, basename='recipes')
router.register(r'movements', InventoryMovementViewSet, basename='movements')

urlpatterns = [
    path('', include(router.urls)),
]