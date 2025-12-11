from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

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


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SmallPageNumberPagination
    def get_queryset(self):
        return Notification.objects.filter(to_user=self.request.user)

    @action(detail=False, methods=["get"], url_path="recent")
    def recent_activity(self, request):
        notifications = self.get_queryset().order_by("-send_date")[:5]
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"], url_path="all")
    def all_notifications(self, request):
        queryset = self.get_queryset().order_by("-send_date")
        
        # Aquí aplicamos la paginación manualmente
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Si por alguna razón no se puede paginar (poco común), devuelves todo
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)