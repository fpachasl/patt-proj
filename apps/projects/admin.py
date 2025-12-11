from django.contrib import admin
from apps.documents.models import Document
from apps.subadmin import RootSubAdmin, SubAdmin
from apps.tasks.models import Task
from .models import (
    Project, ProjectType, ProjectState, ProjectPriority,
    ProjectLeader, ProjectArea, ProjectAreaMember, AreaLeader
)

# === Sub Admin ===
class DocumentSubAdmin(SubAdmin):
    model = Document
    extra = 0
    list_display = ('name', 'document_type', 'uploaded_by', 'upload_date')
    search_fields = ('name', 'uploaded_by__username')
    autocomplete_fields = ['document_type', 'uploaded_by', 'project', 'area']
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')
    readonly_fields = ['upload_date']

class TaskSubAdmin(SubAdmin):
    model = Task
    list_display = ('title', 'task_state', 'assigned_user', 'start_date', 'end_date')
    search_fields = ['title', 'assigned_user__username']
    list_filter = ['task_state']
    autocomplete_fields = ['task_state', 'assigned_user', 'area']
    extra = 0
    subadmins = [DocumentSubAdmin]

# === Inlines ===

class ProjectLeaderInline(admin.TabularInline):
    model = ProjectLeader
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')

    extra = 1
    autocomplete_fields = ['leader']

class ProjectAreaInline(admin.TabularInline):
    model = ProjectArea
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')
    
    extra = 1

class AreaLeaderInline(admin.TabularInline):
    model = AreaLeader
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')
    
    extra = 1
    autocomplete_fields = ['leader']

class ProjectAreaMemberInline(admin.TabularInline):
    model = ProjectAreaMember
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')
    
    extra = 1
    autocomplete_fields = ['user']

    
# === Admins ===

@admin.register(Project)
class ProjectAdmin(RootSubAdmin):
    list_display = ('name', 'project_type', 'project_state', 'start_date', 'end_date', 'company')
    list_filter = ('project_state', 'project_type', 'priority', 'company')
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')
    search_fields = ('name', 'description')
    autocomplete_fields = ['company', 'project_state', 'project_type', 'priority']
    inlines = [ProjectLeaderInline, ProjectAreaInline]
    subadmins = [TaskSubAdmin]

    
@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(ProjectState)
class ProjectStateAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(ProjectPriority)
class ProjectPriorityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(ProjectArea)
class ProjectAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'project')
    search_fields = ('name',)
    autocomplete_fields = ['project']
    inlines = [AreaLeaderInline, ProjectAreaMemberInline]


@admin.register(ProjectLeader)
class ProjectLeaderAdmin(admin.ModelAdmin):
    list_display = ('project', 'leader', 'is_main')
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')

    list_filter = ('is_main',)
    autocomplete_fields = ['project', 'leader']
    search_fields = ('project__name', 'leader__username')


@admin.register(ProjectAreaMember)
class ProjectAreaMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'area', 'role')
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')


    autocomplete_fields = ['user', 'area']
    search_fields = ('user__username', 'area__name')


@admin.register(AreaLeader)
class AreaLeaderAdmin(admin.ModelAdmin):
    list_display = ('leader', 'area', 'role_name')
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')


    autocomplete_fields = ['leader', 'area']
    search_fields = ('leader__username', 'area__name')
