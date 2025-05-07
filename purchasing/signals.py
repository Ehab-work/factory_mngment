from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from users.models import Notification

@receiver(post_save, sender=PurchaseOrder)
def notify_purchase_order_creation(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.employee,
            type='order_status',
            title='New Purchase Order Created',
            message=f'Purchase Order #{instance.id} for {instance.supplier.name} has been created.',
            reference_id=instance.id,
            reference_type='PurchaseOrder'
        )