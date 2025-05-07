from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from purchasing.models import PurchaseOrder, Supplier
from users.models import User
from rest_framework.authtoken.models import Token

class PurchasingTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='admin123', role='admin')
        self.officer = User.objects.create_user(username='officer', password='officer123', role='purchasing_officer')
        self.admin_token = Token.objects.create(user=self.admin)
        self.officer_token = Token.objects.create(user=self.officer)
        self.supplier = Supplier.objects.create(name='Supplier A', contact_info='123456789')

    def test_create_purchase_order_as_officer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.officer_token.key)
        url = reverse('purchase-orders-list')
        data = {
            'supplier': self.supplier.id,
            'quantity': 10,
            'status': 'pending',
            'order_date': '2025-05-06'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 1)