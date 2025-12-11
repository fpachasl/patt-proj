from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.comments.models import Comment
from apps.notifications.models import Notification
from apps.notifications.helpers.notifications_type import get_notification_type
from apps.projects.models import AreaLeader, ProjectLeader

@receiver(post_save, sender=Comment)
def notify_comment_on_task(sender, instance, created, **kwargs):
    if not created or not instance.comment_user:
        return

    task = instance.task
    from_user = instance.comment_user

    notified_users = []

    # 1. Buscar líderes del área si la tarea tiene área
    if task.area:
        area_leaders = AreaLeader.objects.filter(area=task.area)
        for leader_entry in area_leaders:
            if leader_entry.leader != from_user:  # evitar notificar al mismo usuario
                Notification.objects.create(
                    to_user=leader_entry.leader,
                    from_user=from_user,
                    task=task,
                    message=f"{from_user.get_full_name()} comentó en la tarea: {task.title}",
                    type=get_notification_type("comment")
                )
                notified_users.append(leader_entry.leader.id)

    # 2. Si no hay líderes de área, notificar a los líderes del proyecto
    if not task.area or not area_leaders.exists():
        project_leaders = ProjectLeader.objects.filter(project=task.project)
        for leader_entry in project_leaders:
            if leader_entry.leader.id not in notified_users and leader_entry.leader != from_user:
                Notification.objects.create(
                    to_user=leader_entry.leader,
                    from_user=from_user,
                    task=task,
                    message=f"{from_user.get_full_name()} comentó en la tarea: {task.title}",
                    type=get_notification_type("comment")
                )
