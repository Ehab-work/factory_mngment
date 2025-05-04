from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Client, SalesOrder, SalesInvoiceDetail
from inventory.models import Product
from decimal import Decimal

User = get_user_model()

class SalesAppTests(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client_api.force_authenticate(user=self.user)

        self.client_data = Client.objects.create(
            name="Test Client",
            address="123 Street",
            phone_number="0123456789",
            email="client@example.com"
        )

        self.product = Product.objects.create(
            name="Test Product",
            quantity=100,
            unit="pcs",
            unit_price=Decimal("50.00")
        )

        self.sales_order = SalesOrder.objects.create(
            employee=self.user,
            client=self.client_data,
            discount=Decimal("10.00"),
            total_amount=Decimal("90.00"),
            status='pending'
        )

        self.invoice_detail = SalesInvoiceDetail.objects.create(
            sale=self.sales_order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("50.00")
        )

    def test_create_client(self):
        response = self.client_api.post('/sales/clients/', {
            "name": "Client A",
            "address": "Somewhere",
            "phone_number": "1234567890",
            "email": "clienta@example.com"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_sales_orders(self):
        response = self.client_api.get('/sales/sales-orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_sales_invoice_detail(self):
        response = self.client_api.post('/sales/sales-details/', {
            "sale": self.sales_order.id,
            "product": self.product.id,
            "quantity": 1,
            "unit_price": "50.00"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_sales_order_status(self):
        response = self.client_api.patch(f'/sales/sales-orders/{self.sales_order.id}/', {
            "status": "completed"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sales_order.refresh_from_db()
        self.assertEqual(self.sales_order.status, "completed")
