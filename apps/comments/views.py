from rest_framework import viewsets
from .models import Comment, CommentAttachment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # 👈 Para aceptar multipart/form-data

    def get_queryset(self):
        queryset = Comment.objects.select_related('comment_user', 'task').prefetch_related('attachments')
        task_id = self.request.query_params.get('task')
        if task_id:
            queryset = queryset.filter(task__id=task_id)
        return queryset

    def perform_create(self, serializer):
        comment = serializer.save(comment_user=self.request.user)

        # Manejar adjuntos si existen en la solicitud
        files = self.request.FILES.getlist('attachments')
        for file in files:
            CommentAttachment.objects.create(comment=comment, file=file)
