from django.contrib import admin
from .models import DocumentType, Document

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')
    
    search_fields = ('code', 'name')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'document_type', 'uploaded_by', 'project', 'area', 'task', 'upload_date')
    list_filter = ('document_type', 'upload_date', 'project')
    search_fields = ('name', 'uploaded_by__username', 'project__name', 'task__name')
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')
    
    autocomplete_fields = ['document_type', 'uploaded_by', 'project', 'area', 'task']
    readonly_fields = ('upload_date',)
