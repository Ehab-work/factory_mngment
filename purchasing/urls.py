from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, PurchaseOrderViewSet, PurchaseInvoiceDetailViewSet

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet, basename='suppliers')
router.register(r'purchase-orders', PurchaseOrderViewSet, basename='purchase-orders')
router.register(r'invoice-details', PurchaseInvoiceDetailViewSet, basename='invoice-details')

urlpatterns = [
    path('', include(router.urls)),
]