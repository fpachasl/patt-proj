# apps/base/models.py
from django.db import models
from simple_history.models import HistoricalRecords
import uuid
from django.conf import settings

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField("Registrado el", auto_now_add=True)
    updated_at = models.DateTimeField("Última actualización", auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField("Fecha y hora de eliminación", null=True, blank=True)
    
    creator_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="created_items_%(class)s", null=True, blank=True
    )
    modified_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name="modified_items_%(class)s", null=True, blank=True
    )
    deleted_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name="deleted_items_%(class)s", null=True, blank=True
    )

    state = models.BooleanField("Estado activo", default=True)

    class Meta:
        abstract = True
        verbose_name = 'Modelo Base'
        verbose_name_plural = 'Modelos Base'
        ordering = ['-created_at']
