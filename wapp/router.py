from rest_framework import routers
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.comments.views import CommentViewSet
from apps.documents.views import DocumentRagViewSet, DocumentTypeViewSet, DocumentViewSet
from apps.notifications.views import NotificationViewSet
from apps.projects.views import AreaLeaderViewSet, CompanyViewSet, ProjectAreaMemberViewSet, ProjectAreaViewSet, ProjectLeaderViewSet, ProjectPriorityViewSet, ProjectStateViewSet, ProjectTypeViewSet, ProjectViewSet
from apps.tasks.views import TaskStateViewSet, TaskViewSet
from apps.users.views import CompanyUserViewSet, CustomTokenObtainPairView, RoleViewSet, UserActionLogViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user'),
router.register(r'roles', RoleViewSet, basename='role'),
router.register(r'company-users', CompanyUserViewSet, basename='companyuser'),
router.register(r'user-action-logs', UserActionLogViewSet, basename='useractionlog'),

router.register(r'projects', ProjectViewSet, basename='project'),
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'project-priorities', ProjectPriorityViewSet, basename='projectpriority'),
router.register(r'project-types', ProjectTypeViewSet, basename='projecttype'),
router.register(r'project-states', ProjectStateViewSet, basename='projectstate'),
router.register(r'project-leaders', ProjectLeaderViewSet, basename='projectleader'),
router.register(r'project-areas', ProjectAreaViewSet, basename='projectarea'),
router.register(r'project-area-members', ProjectAreaMemberViewSet, basename='projectareamember'),
router.register(r'area-leaders', AreaLeaderViewSet, basename='arealeader'),

router.register(r'tasks', TaskViewSet, basename='task'),
router.register(r'task-states', TaskStateViewSet, basename='taskstate'),

router.register(r'documents', DocumentViewSet, basename='document'),
router.register(r'document-types', DocumentTypeViewSet, basename='documenttype')

router.register(r'comments', CommentViewSet, basename='comment'),
router.register(r'notifications', NotificationViewSet, basename='notification')

router.register(r'document-rag', DocumentRagViewSet, basename='documentrag'),

urlpatterns = [
    # JWT Token URLs
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


all_urls = urlpatterns + router.urls
