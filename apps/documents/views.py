# apps/documents/views.py
from rest_framework import viewsets

from apps.documents.utils import generate_rag_response
from .models import Document, DocumentType
from .serializers import DocumentSerializer, DocumentTypeSerializer
from rest_framework.permissions import IsAuthenticated
from itertools import chain
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action

class SmallPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        }) 
        
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SmallPageNumberPagination
    def get_queryset(self):
        user = self.request.user
        # Obtener proyectos del usuario como líder o miembro
        project_ids = set(chain(
            user.project_leader_roles.values_list('project_id', flat=True),
            user.area_memberships.values_list('area__project_id', flat=True),
            user.assigned_tasks.values_list('project_id', flat=True),
        ))

        return Document.objects.filter(project__id__in=project_ids).order_by("-created_at")
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes = [IsAuthenticated]
    
    
class DocumentRagViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'], url_path="rag")
    def rag(self, request):
        query = request.data.get("message")
        document_ids = request.data.get("documents", [])

        if not query:
            return Response({"error": "No enviaste un mensaje"}, status=400)

        answer = generate_rag_response(query, document_ids=document_ids)

        return Response({
            "message": query,
            "response": answer
        })

    @action(detail=True, methods=['post'], url_path="index")
    def index_document_action(self, request, pk=None):
        from apps.documents.utils import index_document
        from apps.documents.models import Document

        try:
            document = Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Response({"error": "Documento no encontrado"}, status=404)

        index_document(document)

        return Response({"message": "Documento indexado correctamente"})