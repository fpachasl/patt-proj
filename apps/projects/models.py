from django.db import models
from apps.base.models import BaseModel
from apps.company.models import Company
from apps.users.models import User

class ProjectPriority(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name= 'Prioridad'
        verbose_name_plural= 'Prioridades'
        
    def __str__(self):
        return self.name

class ProjectType(BaseModel):
    code = models.CharField(max_length=50, unique=True)  # Ej: 'software', 'infra', 'consulting'
    name = models.CharField(max_length=100)              # Ej: 'Desarrollo de Software'
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name= 'Tipo de proyecto'
        verbose_name_plural= 'Tipos de proyectos'
    def __str__(self):
        return self.name

class ProjectState(BaseModel):
    code = models.CharField(max_length=50, unique=True)  # Ej: "planning"
    name = models.CharField(max_length=100)              # Ej: "En planificación"
    description = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name= 'Estado de proyecto'
        verbose_name_plural= 'Estados de proyectos'
    def __str__(self):
        return self.name

    
class Project(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(auto_now_add=True, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    project_state = models.ForeignKey(ProjectState, on_delete=models.SET_NULL, null=True, related_name='projects')
    project_type = models.ForeignKey(ProjectType, on_delete=models.SET_NULL, null=True, related_name='projects')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='projects', blank=True, null=True)
    priority = models.ForeignKey(ProjectPriority, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['-start_date']
    

class ProjectLeader(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='leaders')
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_leader_roles')
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name= 'Lider de proyecto'
        verbose_name_plural= 'Lideres de proyectos'
        unique_together = ('project', 'leader')
        
    def save(self, *args, **kwargs):
        if self.is_main:
            ProjectLeader.objects.filter(project=self.project, is_main=True).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)
        
class ProjectArea(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='areas')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name= 'Area de proyecto'
        verbose_name_plural= 'Areas de proyectos'
    def __str__(self):
        return f"{self.name} - {self.project.name}"
    
class ProjectAreaMember(BaseModel):
    area = models.ForeignKey(ProjectArea, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='area_memberships')
    role = models.CharField(max_length=100, blank=True, null=True)  # Ej: Desarrollador, Tester, etc.

    class Meta:
        verbose_name= 'Miembro del area'
        verbose_name_plural= 'Miembros de las areas'
        unique_together = ('area', 'user')

    def __str__(self):
        return f"{self.user.get_full_name()} en {self.area.name}"

class AreaLeader(BaseModel):
    area = models.ForeignKey(ProjectArea, on_delete=models.CASCADE, related_name='leaders')
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='area_leader_roles')
    role_name = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name= 'Lider del area'
        verbose_name_plural= 'Lideres de las areas'
        unique_together = ('area', 'leader')

    def __str__(self):
        return f"Líder: {self.leader.get_full_name()} - Área: {self.area.name}"