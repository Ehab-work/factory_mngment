from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, Notification
from django.utils import timezone
from rest_framework.authtoken.models import Token

class UserTests(APITestCase):
    def setUp(self):
        # إنشاء مستخدمين وToken
        self.admin = User.objects.create_user(
            username='admin', password='admin123', role='admin', email='admin@example.com'
        )
        self.user = User.objects.create_user(
            username='user', password='user123', role='worker', email='user@example.com'
        )
        self.admin_token = Token.objects.create(user=self.admin)
        self.user_token = Token.objects.create(user=self.user)

    def test_create_user_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        url = reverse('users-list')
        data = {
            'username': 'newuser',
            'password': 'newuser123',
            'email': 'newuser@example.com',
            'role': 'worker'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(username='newuser').role, 'worker')

    def test_create_user_as_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('users-list')
        data = {
            'username': 'newuser2',
            'password': 'newuser2123',
            'email': 'newuser2@example.com',
            'role': 'worker'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_notification_creation_on_user_create(self):
        Notification.objects.all().delete()  # مسح كل الإشعارات قبل الاختبار
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        url = reverse('users-list')
        data = {
            'username': 'newuser3',
            'password': 'newuser3123',
            'email': 'newuser3@example.com',
            'role': 'worker'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user.username, 'newuser3')  # تغيير recipient إلى user
        self.assertIn('created', notification.message)