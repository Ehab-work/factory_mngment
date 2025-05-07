from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductionOrder, ProductionTask
from users.models import Notification

@receiver(post_save, sender=ProductionOrder)
def notify_production_order_creation(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.employee,
            type='production_status',
            title='New Production Order Created',
            message=f'Production Order #{instance.id} for {instance.product.name} has been created.',
            reference_id=instance.id,
            reference_type='ProductionOrder'
        )

@receiver(post_save, sender=ProductionTask)
def notify_task_assignment(sender, instance, created, **kwargs):
    if created and instance.assigned_to:
        Notification.objects.create(
            user=instance.assigned_to,
            type='task_assignment',
            title='New Task Assigned',
            message=f'You have been assigned a task: {instance.name} for Production Order #{instance.production_order.id}.',
            reference_id=instance.id,
            reference_type='ProductionTask'
        )