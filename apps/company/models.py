from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    ruc = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

