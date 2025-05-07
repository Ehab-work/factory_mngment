from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Notification

@receiver(post_save, sender=User)
def notify_user_creation(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance,
            type='account_status',
            title='Welcome to the System',
            message=f'Your account has been created with role: {instance.role}.'
        )