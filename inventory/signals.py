from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InventoryMovement
from users.models import Notification

@receiver(post_save, sender=InventoryMovement)
def notify_inventory_movement(sender, instance, created, **kwargs):
    if created and instance.moved_by:
        item = instance.product or instance.raw_material
        Notification.objects.create(
            user=instance.moved_by,
            type='order_status',
            title='Inventory Movement Recorded',
            message=f'{instance.move_type} {instance.quantity} of {item} on {instance.move_date}.',
            reference_id=instance.id,
            reference_type='InventoryMovement'
        )