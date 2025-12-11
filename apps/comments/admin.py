from django.contrib import admin

from apps.documents.models import Document
from .models import Comment, CommentAttachment

class CommentAttachmentInline(admin.TabularInline):
    model = CommentAttachment
    extra = 0
    fields = ('file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_user', 'task', 'comment_date', 'is_internal')
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')

    list_filter = ('is_internal', 'comment_date')
    search_fields = ('content', 'comment_user__username', 'task__title')
    autocomplete_fields = ['comment_user', 'task']
    date_hierarchy = 'comment_date'

    inlines = [CommentAttachmentInline]  