from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

class RawMaterial(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    unit = models.CharField(max_length=255)
    avg_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    stock_quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    unit = models.CharField(max_length=255)
    worst_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    type = models.CharField(max_length=255, default='standard')

    def __str__(self):
        return self.name

class InventoryMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Inbound'),
        ('OUT', 'Outbound'),
    ]
    MATERIAL_TYPES = [
        ('raw', 'Raw Material'),
        ('product', 'Product'),
    ]
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    material_id = models.PositiveIntegerField()
    quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.material_type} | {self.movement_type} | {self.quantity}"

class RatioOfProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    ratio = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    def __str__(self):
        return f"{self.product.name} - {self.raw_material.name} - {self.ratio}"

class MaterialRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    ]
    
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='material_requests', on_delete=models.CASCADE)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='material_approvals', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Request for {self.raw_material.name} - {self.quantity} {self.raw_material.unit}"