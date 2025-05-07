from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SalesOrder
from users.models import Notification

@receiver(post_save, sender=SalesOrder)
def notify_sales_order_creation(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.employee,
            type='order_status',
            title='New Sales Order Created',
            message=f'Sales Order #{instance.id} for {instance.client.name} has been created.',
            reference_id=instance.id,
            reference_type='SalesOrder'
        )