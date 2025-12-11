from django.db import models
from apps.base.models import BaseModel
from apps.projects.models import Project
from apps.tasks.models import Task
from apps.users.models import User

class NotificationType(BaseModel):
    code = models.CharField(max_length=20, unique=True)  # Ej: 'info', 'success'
    name = models.CharField(max_length=50)               # Ej: 'Información'
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name= 'Tipo de notificacion'
        verbose_name_plural= 'Tipos de notificaciones'
        
    def __str__(self):
        return self.name

class Notification(BaseModel):
    type = models.ForeignKey(NotificationType, on_delete=models.SET_NULL, null=True, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    send_date = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True,)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')

    class Meta:
        verbose_name= 'Notificacion'
        verbose_name_plural= 'Notificaciones'
        ordering = ['-created_at']

    def __str__(self):
        return f"Notificación para {self.to_user.username} - {self.type.name if self.type else 'Sin tipo'}"
