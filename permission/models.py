from django.db import models

from blog.models import BaseAbstractModel

class PermissionName(models.TextChoices):
    READ = ('read', 'Read')
    EDIT = ('edit', 'Edit')

class Permission(BaseAbstractModel):

    name = models.CharField(("name"), choices=PermissionName, max_length=10, default=None)
    
    class Meta:
        db_table = "permissions"
        verbose_name = ("Permission")
        verbose_name_plural = ("Permissions")

    def __str__(self):
        return self.name