from django.db import models
from apps.base.models import BaseModel
from apps.projects.models import Project, ProjectArea
from apps.users.models import User
# Create your models here.
class TaskState(BaseModel):
    code = models.CharField(max_length=50, unique=True)  # Ej: planning, in_progress, completed
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name= 'Estado de las tarea'
        verbose_name_plural= 'Estado de las tareas'
    
    def __str__(self):
        return self.name

class Task(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    task_state = models.ForeignKey(TaskState, on_delete=models.SET_NULL, null=True, related_name='tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    area = models.ForeignKey(ProjectArea, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='leaderassigned_tasks')
    class Meta:
        verbose_name= 'Tarea'
        verbose_name_plural= 'Tareas'
        
    
    def __str__(self):
        return self.title
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_assigned_user = self.assigned_user
        self.original_task_state = self.task_state
