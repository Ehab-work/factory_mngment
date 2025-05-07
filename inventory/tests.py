from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from inventory.models import Product, InventoryMovement
from users.models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token

class InventoryTests(APITestCase):
    def setUp(self):
        # إنشاء مستخدمين وToken
        self.admin = User.objects.create_user(username='admin', password='admin123', role='admin')
        self.store_keeper = User.objects.create_user(username='storekeeper', password='store123', role='store_keeper')
        self.worker = User.objects.create_user(username='worker', password='worker123', role='worker')
        self.admin_token = Token.objects.create(user=self.admin)
        self.store_keeper_token = Token.objects.create(user=self.store_keeper)
        self.worker_token = Token.objects.create(user=self.worker)
        # إنشاء منتج
        self.product = Product.objects.create(name='Product A', price=100, quantity=50)

    def test_create_product_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        url = reverse('products-list')
        data = {'name': 'Product B', 'price': 200, 'quantity': 30}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(name='Product B').price, 200)

    def test_create_product_as_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.worker_token.key)
        url = reverse('products-list')
        data = {'name': 'Product C', 'price': 300, 'quantity': 20}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_inventory_movement_as_store_keeper(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_keeper_token.key)
        url = reverse('movements-list')
        data = {
            'product': self.product.id,
            'quantity': 10,
            'move_type': 'out',
            'reference_type': 'manual',
            'notes': 'Test movement'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InventoryMovement.objects.count(), 1)
        movement = InventoryMovement.objects.first()
        self.assertEqual(movement.quantity, 10)
        self.assertEqual(movement.moved_by, self.store_keeper)

    def test_inventory_movement_as_non_store_keeper(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.worker_token.key)
        url = reverse('movements-list')
        data = {
            'product': self.product.id,
            'quantity': 5,
            'move_type': 'in',
            'reference_type': 'manual'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)