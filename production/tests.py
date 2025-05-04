from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import ProductionOrder, Task

User = get_user_model()

class ProductionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username='admin', password='pass', role='admin')
        self.worker = User.objects.create_user(username='worker', password='pass', role='worker')
        self.supervisor = User.objects.create_user(username='supervisor', password='pass', role='supervisor')

        self.order = ProductionOrder.objects.create(name='Test Order', supervisor=self.supervisor)
        self.task = Task.objects.create(order=self.order, assigned_to=self.worker, description='Test Task')

    def test_admin_can_create_order(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/production/orders/', {
            'name': 'New Order',
            'supervisor': self.supervisor.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_worker_can_only_view_own_tasks(self):
        self.client.force_authenticate(user=self.worker)
        response = self.client.get('/api/production/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for task in response.data:
            self.assertEqual(task['assigned_to'], self.worker.id)

    def test_worker_cannot_delete_task(self):
        self.client.force_authenticate(user=self.worker)
        response = self.client.delete(f'/api/production/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_supervisor_can_update_task(self):
        self.client.force_authenticate(user=self.supervisor)
        response = self.client.patch(f'/api/production/tasks/{self.task.id}/', {'status': 'completed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'completed')
