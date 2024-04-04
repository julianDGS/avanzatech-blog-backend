from django.db import models

from blog.models import BaseAbstractModel

class PermissionName(models.TextChoices):
    READ = ('read', 'Read')
    EDIT = ('edit', 'Edit')

class CategoryName(models.TextChoices):
    PUBLIC = ('public', 'Public')
    AUTHENTICATE = ('auth', 'Authenticate')
    TEAM = ('team', 'Team')
    AUTHOR = ('author', 'Author')

class Permission(BaseAbstractModel):

    name = models.CharField(("name"), choices=PermissionName, unique=True, max_length=10, default=None)
    
    class Meta:
        db_table = "permissions"
        verbose_name = ("Permission")
        verbose_name_plural = ("Permissions")

    def __str__(self):
        return self.name
    
class Category(BaseAbstractModel):

    name = models.CharField(("name"), choices=CategoryName, unique=True, max_length=20, default=None)
    
    class Meta:
        db_table = "categories"
        verbose_name = ("Categories")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.name