from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, SalesOrderViewSet, SalesInvoiceDetailViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'sales-orders', SalesOrderViewSet, basename='sales-orders')
router.register(r'invoice-details', SalesInvoiceDetailViewSet, basename='invoice-details')

urlpatterns = [
    path('', include(router.urls)),
]