from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            email='admin@example.com',
            role='admin'
        )
        # Create regular user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            role='worker',
            phone_number='+201234567890',
            national_id='12345678901234',
            age=30,
            address='Test Address'
        )

    def test_login(self):
        """Test user login and token acquisition"""
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_user_register_as_admin(self):
        """Test user registration - only admin should be able to create users"""
        url = reverse('register')
        
        # First try without authentication
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'password2': 'newpass123',
            'email': 'new@example.com',
            'role': 'worker'
        }
        response = self.client.post(url, data, format='json')
        # Should fail because not authenticated as admin
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Now login as admin
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(username='newuser').role, 'worker')

    def test_user_profile_view(self):
        """Test user can view their profile"""
        url = reverse('user-profile')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_user_profile_update(self):
        """Test user can update their profile"""
        url = reverse('user-profile')
        self.client.force_authenticate(user=self.user)
        data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'address': 'New Address'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.address, 'New Address')

    def test_change_user_role(self):
        """Test admin can change user role"""
        url = reverse('change-user-role', kwargs={'pk': self.user.id})
        
        # Try as regular user first
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, {'role': 'sales_rep'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Now try as admin
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(url, {'role': 'sales_rep'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, 'sales_rep')

    def test_user_stats(self):
        """Test admin can view user statistics"""
        url = reverse('user-stats')
        
        # Try as regular user first
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Now try as admin
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_users'], 2)
        self.assertIn('users_by_role', response.data)

    def test_user_validation(self):
        """Test user validation for registration"""
        url = reverse('register')
        self.client.force_authenticate(user=self.admin_user)
        
        # Test invalid national ID
        data = {
            'username': 'baduser1',
            'password': 'badpass123',
            'password2': 'badpass123',
            'email': 'bad1@example.com',
            'role': 'worker',
            'national_id': '123'  # Too short
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test invalid phone number
        data = {
            'username': 'baduser2',
            'password': 'badpass123',
            'password2': 'badpass123',
            'email': 'bad2@example.com',
            'role': 'worker',
            'phone_number': '123'  # Invalid format
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test invalid age
        data = {
            'username': 'baduser3',
            'password': 'badpass123',
            'password2': 'badpass123',
            'email': 'bad3@example.com',
            'role': 'worker',
            'age': 15  # Too young
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)