from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from apps.notifications.helpers.notifications_type import get_notification_type
from apps.notifications.models import Notification
from apps.projects.models import Project


@receiver(pre_save, sender=Project)
def set_old_project_state(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous = Project.objects.get(pk=instance.pk)
            instance._old_project_state = previous.project_state
        except Project.DoesNotExist:
            instance._old_project_state = None
            

@receiver(post_save, sender=Project)
def notify_project_state_change(sender, instance, created, **kwargs):
    if not created:
        old_state = getattr(instance, "_old_project_state", None)
        if old_state and old_state != instance.project_state:
            for leader in instance.leaders.all():
                Notification.objects.create(
                    to_user=leader.leader,
                    from_user=None,
                    message=f"El estado del proyecto '{instance.name}' cambió de {old_state.name} a: {instance.project_state.name}",
                    type=get_notification_type("state_change")
                )
