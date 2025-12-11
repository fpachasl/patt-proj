from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.base.models import BaseModel
from apps.company.models import Company

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Ej: admin, leader, member
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

    
class User(AbstractUser, BaseModel):

    cellphone = models.CharField(max_length=15, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.username}"
    
class CompanyUser(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role_in_company = models.CharField(max_length=50, blank=True, null=True)
    joined_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('company', 'user')

class UserActionLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Inicio de sesión'),
        ('logout', 'Cierre de sesión'),
        ('create', 'Creación'),
        ('update', 'Actualización'),
        ('delete', 'Eliminación'),
        ('view', 'Visualización'),
        ('download', 'Descarga'),
        ('upload', 'Subida'),
        ('assign', 'Asignación'),
        ('change_state', 'Cambio de estado'),
        ('custom', 'Personalizado'),  # Para texto libre en metadata
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, default='custom')
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, null=True)  # Contexto adicional

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"