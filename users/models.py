from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('production_supervisor', 'Production Supervisor'),
        ('worker', 'Worker'),
        ('store_keeper', 'Store Keeper'),
        ('sales_rep', 'Sales Representative'),
        ('sales_supervisor', 'Sales Supervisor'),
        ('purchasing_officer', 'Purchasing Officer'),
    ]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='worker')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    last_activity = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

class Notification(models.Model):
    TYPE_CHOICES = [
        ('order_status', 'Order Status'),
        ('task_assignment', 'Task Assignment'),
        ('production_status', 'Production Status'),
        ('account_status', 'Account Status'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    reference_id = models.PositiveIntegerField(blank=True, null=True)
    reference_type = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.title} for {self.user.username}"