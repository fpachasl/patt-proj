from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Role, User, CompanyUser, UserActionLog

# -------------------------------
# Rol de Usuario
# -------------------------------
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')
    


# -------------------------------
# Usuario (Personalizado)
# -------------------------------
@admin.register(User)
class CustomUserAdmin(DefaultUserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')
    
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('cellphone', 'role')
        }),
    )


# -------------------------------
# Relación Empresa - Usuario
# -------------------------------
@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'role_in_company', 'joined_at')
    search_fields = ('user__username', 'company__name')
    list_filter = ('joined_at', 'company')
    autocomplete_fields = ('user', 'company')
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')
    


# -------------------------------
# Log de acciones de usuario
# -------------------------------
@admin.register(UserActionLog)
class UserActionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'short_metadata')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'action', 'metadata')
    readonly_fields = ('user', 'action', 'timestamp', 'metadata')
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')
    

    def short_metadata(self, obj):
        return str(obj.metadata)[:75] + '...' if obj.metadata else "-"
    short_metadata.short_description = 'Metadata'
