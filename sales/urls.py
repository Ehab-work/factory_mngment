from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, SalesOrderViewSet, SalesInvoiceDetailViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'sales-orders', SalesOrderViewSet)
router.register(r'sales-details', SalesInvoiceDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]