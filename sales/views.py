from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Client, SalesOrder, SalesInvoiceDetail
from .serializers import ClientSerializer, SalesOrderSerializer, SalesInvoiceDetailSerializer
from users.permissions import IsManagerOrReadOnly

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.prefetch_related('details').select_related('employee', 'client').all()
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]

class SalesInvoiceDetailViewSet(viewsets.ModelViewSet):
    queryset = SalesInvoiceDetail.objects.select_related('sale', 'product').all()
    serializer_class = SalesInvoiceDetailSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]