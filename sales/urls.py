from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', views.ClientRetrieveUpdateDestroyView.as_view(), name='client-detail'),

    path('sales-orders/', views.SalesOrderListCreateView.as_view(), name='salesorder-list-create'),
    path('sales-orders/<int:pk>/', views.SalesOrderRetrieveUpdateDestroyView.as_view(), name='salesorder-detail'),

    path('sales-details/', views.SalesInvoiceDetailListCreateView.as_view(), name='salesdetail-list-create'),
    path('sales-details/<int:pk>/', views.SalesInvoiceDetailRetrieveUpdateDestroyView.as_view(), name='salesdetail-detail'),
] 
