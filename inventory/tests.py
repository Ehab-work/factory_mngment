from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import RawMaterial, Unit, MaterialRequest

User = get_user_model()

class MaterialRequestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        unit = Unit.objects.create(name='kg')
        self.raw = RawMaterial.objects.create(name='Iron', unit=unit, quantity=100)

    def test_create_request(self):
        self.client.login(username='testuser', password='12345')
        req = MaterialRequest.objects.create(requested_by=self.user, raw_material=self.raw, quantity=10)
        self.assertEqual(req.status, 'pending')