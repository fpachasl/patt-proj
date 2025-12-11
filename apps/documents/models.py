from django.db import models
from apps.base.models import BaseModel
from apps.projects.models import Project, ProjectArea
from apps.tasks.models import Task
from apps.users.models import User
from pgvector.django import VectorField

class DocumentType(BaseModel):
    code = models.CharField(max_length=50, unique=True)  # Ej: 'pdf', 'docx', 'xls', etc.
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name= 'Tipo de documento'
        verbose_name_plural= 'Tipos de documentos'

    def __str__(self):
        return self.name

class Document(BaseModel):
    name = models.CharField(max_length=200, null=True, blank=True,)
    file = models.FileField(upload_to='documents/', null=True, blank=True,)
    upload_date = models.DateTimeField(auto_now_add=True)

    document_type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_documents')
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    area = models.ForeignKey(ProjectArea, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')

    class Meta:
        verbose_name= 'Documento'
        verbose_name_plural= 'Documentos'

    def __str__(self):
        return self.name
    
    
class DocumentEmbedding(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="embedding")
    embedding = VectorField(dimensions=384)  # dimensión típica de SBERT
    text = models.TextField()  # chunk de texto extraído del documento

    def __str__(self):
        return f"Embedding for {self.document.name}"