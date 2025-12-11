from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.notifications.helpers.notifications_type import get_notification_type
from apps.tasks.models import Task
from apps.notifications.models import Notification

@receiver(post_save, sender=Task)
def notify_task_assignment(sender, instance, created, **kwargs):

    if created and instance.assigned_user:
        Notification.objects.create(
            to_user=instance.assigned_user,
            from_user=instance.assigned_by,
            message=f"Se te ha asignado la nueva tarea: {instance.title}",
            task=instance,
            type=get_notification_type("info")
        )
    elif not created and instance.assigned_user:
        if instance.original_assigned_user != instance.assigned_user:
            Notification.objects.create(
                to_user=instance.assigned_user,
                from_user=instance.assigned_by,
                message=f"Se te ha reasignado la tarea: {instance.title}",
                task=instance,
                type=get_notification_type("info")
            )

@receiver(post_save, sender=Task)
def notify_task_state_change(sender, instance, created, **kwargs):
    if not created and instance.task_state and instance.original_task_state != instance.task_state:
        Notification.objects.create(
            to_user=instance.assigned_user,
            from_user=instance.assigned_by,
            message=f"La tarea '{instance.title}' cambió de estado a: {instance.task_state.name}",
            task=instance,
            type=get_notification_type("info")
        )