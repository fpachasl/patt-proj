from django.db import models
from apps.base.models import BaseModel
from apps.tasks.models import Task
from apps.users.models import User
# Create your models here.
class Comment(BaseModel):
    content = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    
    comment_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    
    is_internal = models.BooleanField(default=True, help_text="Si el comentario es visible solo para el equipo interno")
    
    class Meta:
        verbose_name= 'Comentario'
        verbose_name_plural= 'Comentarios'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Comentario de {self.comment_user} en {self.task}"
    
class CommentAttachment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='comments/attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name= 'Archivo Comentario'
        verbose_name_plural= 'Archivos Comentarios'

    def __str__(self):
        return f"Archivo en {self.comment.id}"