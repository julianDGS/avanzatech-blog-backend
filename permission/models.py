from django.db import models

from blog.models import BaseAbstractModel, BlogPost

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
    

class PostPermission(models.Model):
    
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    class Meta:
        db_table = 'post_category_permissions'
        constraints = [
            models.UniqueConstraint(fields=['post', 'category'], name='unique_post_category')
        ]

    def __str__(self):
        return f'{self.post}, with: {self.category} and {self.permission}'
