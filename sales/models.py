from django.db import models
from django.conf import settings
from inventory.models import Product
from django.core.validators import MinValueValidator
from decimal import Decimal

class Client(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales_orders')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sales_orders')
    sale_date = models.DateField(auto_now_add=True)
    
    discount = models.DecimalField(  # ✅ خصم
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    status = models.CharField(  # ✅ حالة
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )

    def __str__(self):
        return f"Sales Order #{self.id} - {self.client.name}"

class SalesInvoiceDetail(models.Model):
    sale = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return f"Invoice Detail for Sale #{self.sale.id}, Product: {self.product.name}"
