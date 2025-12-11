# apps/documents/serializers.py
from rest_framework import serializers

from apps.projects.models import Project, ProjectArea
from apps.projects.serializers import ProjectDetailSerializer
from apps.tasks.models import Task
from .models import Document, DocumentType

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType 
        fields = '__all__'
        
        
class DocumentSerializer(serializers.ModelSerializer):
    project = ProjectDetailSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), source="project", write_only=True)

    area = serializers.PrimaryKeyRelatedField(queryset=ProjectArea.objects.all(), required=False, allow_null=True)
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False, allow_null=True)

    document_type = DocumentTypeSerializer(read_only=True)
    document_type_id = serializers.PrimaryKeyRelatedField(queryset=DocumentType.objects.all(), source="document_type", write_only=True, allow_null=True, required=False)

    class Meta:
        model = Document
        fields = [
            'id',
            'name',
            'file',
            'project', 'project_id',
            'area',
            'task',
            'document_type', 'document_type_id',
            'uploaded_by',
            'created_at',
            'upload_date'
        ]
