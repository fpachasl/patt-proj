from django.contrib import admin

from apps.documents.models import Document
from .models import TaskState, Task


@admin.register(TaskState)
class TaskStateAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_state', 'project', 'area', 'assigned_user', 'start_date', 'end_date')
    list_filter = ('task_state', 'project', 'area')
    search_fields = ('title', 'description', 'assigned_user__username', 'project__name')
    autocomplete_fields = ['task_state', 'project', 'area', 'assigned_user']
    date_hierarchy = 'start_date'
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')

