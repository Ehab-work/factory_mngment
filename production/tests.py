from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from production.models import ProductionOrder, ProductionTask
from inventory.models import Product
from users.models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token

class ProductionTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='admin123', role='admin')
        self.supervisor = User.objects.create_user(username='supervisor', password='super123', role='production_supervisor')
        self.worker = User.objects.create_user(username='worker', password='worker123', role='worker')
        self.admin_token = Token.objects.create(user=self.admin)
        self.supervisor_token = Token.objects.create(user=self.supervisor)
        self.worker_token = Token.objects.create(user=self.worker)
        self.product = Product.objects.create(name='Product A', price=100, stock=50)

    def test_create_production_order_as_supervisor(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.supervisor_token.key)
        url = reverse('production-orders-list')
        data = {
            'product': self.product.id,
            'quantity': '20.00',
            'status': 'pending',
            'expected_end_date': '2025-05-15'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductionOrder.objects.count(), 1)

    def test_create_production_task_as_supervisor(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.supervisor_token.key)
        order = ProductionOrder.objects.create(
            product=self.product,
            quantity='20.00',
            status='pending',
            employee=self.supervisor,
            expected_end_date=timezone.now() + timezone.timedelta(days=5)
        )
        url = reverse('tasks-list')
        data = {
            'production_order': order.id,
            'name': 'Task 1',
            'description': 'Test task description',
            'assigned_to': self.worker.id,
            'status': 'pending',
            'end_date': '2025-05-10T12:00:00Z'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductionTask.objects.count(), 1)