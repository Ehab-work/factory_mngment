from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
from users.models import User

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])
    stock = models.PositiveIntegerField(default=0)  # أضفنا stock

    def __str__(self):
        return self.name

class RawMaterial(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])
    avg_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])

    def __str__(self):
        return self.name

class RecipeOfProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='recipes')
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, related_name='recipes')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        unique_together = ['product', 'raw_material']

    def __str__(self):
        return f"{self.product.name} - {self.raw_material.name}"
    
class InventoryMovement(models.Model):
    MOVE_TYPE_CHOICES = [
        ('in', 'In'),
        ('out', 'Out'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='inventory_movements')
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, null=True, blank=True, related_name='inventory_movements')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    move_type = models.CharField(max_length=10, default='in')
    moved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='inventory_movements_moved')
    move_date = models.DateTimeField(auto_now_add=True)
    reference_type = models.CharField(max_length=50, blank=True, null=True)
    reference_id = models.PositiveIntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.move_type} - {self.quantity} of {self.product or self.raw_material}"