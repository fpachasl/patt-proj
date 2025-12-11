from django.contrib import admin
from .models import NotificationType, Notification

@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')
    

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'type', 'message', 'is_read', 'send_date')
    list_filter = ('type', 'is_read', 'send_date')
    search_fields = ('message', 'from_user__username', 'to_user', 'type__name')
    autocomplete_fields = ['from_user', 'to_user', 'task', 'type']
    date_hierarchy = 'send_date'
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')
    
