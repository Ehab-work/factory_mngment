from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from sales.models import SalesOrder, Client
from users.models import User
from rest_framework.authtoken.models import Token

class SalesTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='admin123', role='admin')
        self.admin_token = Token.objects.create(user=self.admin)
        self.client_instance = Client.objects.create(name='Client A', contact_info='987654321')

    def test_create_sales_order_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        url = reverse('sales-orders-list')
        data = {
            'client': self.client_instance.id,
            'quantity': 5,
            'status': 'pending',
            'order_date': '2025-05-06'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SalesOrder.objects.count(), 1)