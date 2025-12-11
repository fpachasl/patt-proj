from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'ruc')  # Ajusta según tus campos
    search_fields = ('name', 'ruc')
    exclude = ('created_at', 'updated_at', 'deleted_at', 'creator_user', 'modified_user', 'deleted_user', 'state')
    
