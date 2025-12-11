# apps/tasks/views.py
from rest_framework import viewsets

from apps.projects.models import ProjectLeader
from .models import Task, TaskState
from .serializers import TaskAssignedSerializer, TaskDetailSerializer, TaskSerializer, TaskStateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=["get"], url_path="assigned")
    def assigned(self, request):
        user = request.user
        tasks = Task.objects.filter(assigned_user=user).select_related("project", "task_state")
        serializer = TaskAssignedSerializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"], url_path="detail")
    def task_detail(self, request, pk=None):
        try:
            task = Task.objects.select_related(
                'project', 'area', 'assigned_user', 'assigned_by', 'task_state'
            ).get(pk=pk)
        except Task.DoesNotExist:
            return Response({"detail": "Tarea no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        if task.assigned_user != request.user and not request.user.role.id == 1:
            return Response({"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN)

        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], url_path="update-state")
    def update_state(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"detail": "Tarea no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        if task.assigned_user != request.user and not request.user.role.name == "admin":
            return Response({"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN)

        task_state_id = request.data.get("task_state")
        if not task_state_id:
            return Response({"detail": "Falta 'task_state'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from apps.tasks.models import TaskState
            new_state = TaskState.objects.get(pk=task_state_id)
            task.task_state = new_state
            task.save()
        except TaskState.DoesNotExist:
            return Response({"detail": "Estado no válido."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Estado actualizado correctamente."}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"], url_path="by-project/(?P<project_id>[^/.]+)")
    def by_project(self, request, project_id=None):
        user = request.user
        role = getattr(user.role, "name", "").lower()

        # Verificar si es líder del proyecto
        is_leader = ProjectLeader.objects.filter(project_id=project_id, leader=user).exists()

        if role == "admin" or is_leader:
            # Admins y líderes ven todo
            tasks = Task.objects.filter(project_id=project_id)
        else:
            # Miembros ven solo las tareas asignadas o no asignadas
            tasks = Task.objects.filter(
                Q(project_id=project_id) & (Q(assigned_user=user) | Q(assigned_user__isnull=True))
            )

        serializer = TaskAssignedSerializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["patch"], url_path="assign-user")
    def assign_user(self, request, pk=None):
        try:
            task_id = request.data.get("task_id")
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response({"detail": "Tarea no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role.id not in [1, 2]:
            return Response({"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get("assigned_user")
        if not user_id:
            return Response({"detail": "Falta 'assigned_user'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from apps.users.models import User
            user = User.objects.get(pk=user_id)
            task.assigned_user = user
            task.assigned_by = request.user
            task.save()
            return Response({"detail": "Tarea asignada correctamente."})
        except User.DoesNotExist:
            return Response({"detail": "Usuario no válido."}, status=status.HTTP_400_BAD_REQUEST)

class TaskStateViewSet(viewsets.ModelViewSet):
    queryset = TaskState.objects.all()
    serializer_class = TaskStateSerializer
    permission_classes = [IsAuthenticated]