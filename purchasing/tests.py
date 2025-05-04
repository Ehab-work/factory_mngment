from django.test import TestCase
from django.contrib.auth import get_user_model
from purchasing.models import Supplier, PurchaseOrder, PurchaseOrderItem
from inventory.models import Product
from datetime import date

User = get_user_model()

class PurchasingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            address='123 Test St',
            phone_number='0123456789',
            email='supplier@test.com'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            quantity=100
        )
        self.purchase_order = PurchaseOrder.objects.create(
            employee=self.user,
            supplier=self.supplier,
            order_date=date.today(),
            total_amount=100.00,
            status='pending'
        )
        self.item = PurchaseOrderItem.objects.create(
            purchase_order=self.purchase_order,
            product=self.product,
            quantity=5,
            unit_price=20.00
        )

    def test_purchase_order_created(self):
        self.assertEqual(PurchaseOrder.objects.count(), 1)
        self.assertEqual(self.purchase_order.total_amount, 100.00)
        self.assertEqual(self.purchase_order.status, 'pending')

    def test_purchase_order_item(self):
        self.assertEqual(PurchaseOrderItem.objects.count(), 1)
        self.assertEqual(self.item.quantity, 5)
        self.assertEqual(self.item.product, self.product)

    def test_supplier_str(self):
        self.assertEqual(str(self.supplier), 'Test Supplier')

    def test_purchase_order_str(self):
        self.assertIn(str(self.purchase_order.id), str(self.purchase_order))

    def test_purchase_order_item_str(self):
        self.assertIn(self.product.name, str(self.item))
