from apps.notifications.models import NotificationType


def get_notification_type(code):
    return NotificationType.objects.filter(code=code).first()
