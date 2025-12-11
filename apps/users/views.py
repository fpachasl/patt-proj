# apps/users/views.py
from rest_framework import viewsets
from .models import CompanyUser, Role, User, UserActionLog
from .serializers import CompanyUserSerializer, RoleSerializer, UserActionLogSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # puedes cambiar a AllowAny si lo necesitas

    @action(detail=False, methods=["get"], url_path="profile")
    def get_profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"], url_path="by-id")
    def get_user_by_id(self, request, pk=None):
        if str(request.user.id) != pk and not request.user.role.name == "admin":
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)

        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=["put", "patch"], url_path="update-profile")
    def update_profile(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


class CompanyUserViewSet(viewsets.ModelViewSet):
    queryset = CompanyUser.objects.select_related('company', 'user')
    serializer_class = CompanyUserSerializer
    permission_classes = [IsAuthenticated]

class UserActionLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Solo lectura, útil para auditoría
    """
    queryset = UserActionLog.objects.select_related('user')
    serializer_class = UserActionLogSerializer
    permission_classes = [IsAuthenticated]