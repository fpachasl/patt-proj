# apps/tasks/serializers.py
from rest_framework import serializers

from apps.projects.serializers import ProjectAreaSerializer, ProjectDetailSerializer
from apps.users.serializers import UserSerializer
from .models import Task, TaskState

class TaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields =  '__all__'


class TaskStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskState
        fields = '__all__'
        
class TaskAssignedSerializer(serializers.ModelSerializer):
    assigned_user = UserSerializer(read_only=True)
    assigned_by = UserSerializer(read_only=True)
    project = ProjectDetailSerializer(read_only=True)
    task_state = TaskStateSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id", "title", "description", "start_date", "end_date",
            "project", "task_state", "assigned_user", "assigned_by", "created_at", "updated_at"
        ]
    
class TaskDetailSerializer(serializers.ModelSerializer):
    project = ProjectDetailSerializer(read_only=True)
    area = ProjectAreaSerializer(read_only=True)
    task_state = TaskStateSerializer(read_only=True)
    assigned_user = UserSerializer(read_only=True)
    assigned_by = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        