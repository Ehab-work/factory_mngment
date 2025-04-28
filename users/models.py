from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('sales_rep', 'Sales Representative'),
        ('sales_supervisor', 'Sales Supervisor'),
        ('purchasing_officer', 'Purchasing Officer'),
        ('worker', 'Worker'),
        ('production_supervisor', 'Production Supervisor'),
        ('store_keeper', 'Store Keeper'),
    ]

    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    address = models.CharField(max_length=255, blank=True, null=True)
    salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    age = models.IntegerField(null=True, blank=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    national_id = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"