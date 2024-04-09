from django.db import transaction
from rest_framework import serializers

from ..models import BlogPost
from permission.models import PostPermission, CategoryName, PermissionName, Category, Permission

class BlogPostSerializer(serializers.ModelSerializer):   
    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'content', 'author')

class BlogPostCreateSerializer(serializers.ModelSerializer):
    permissions = serializers.DictField(child=serializers.CharField(allow_null=True), write_only=True, required=True)

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'content', 'author', 'permissions')


    def validate_permissions(self, permissions: dict):
        allowed_categories = [choice for choice, _ in CategoryName.choices]
        allowed_perms = [choice for choice, _ in PermissionName.choices] + [None]
        if len(permissions) != len(allowed_categories):
            raise serializers.ValidationError(f"Missing permission for some category.")
        for category, perm in permissions.items():
            if category not in allowed_categories:
                raise serializers.ValidationError(f"'{category}' is not a valid category.")
            if perm not in allowed_perms:
                raise serializers.ValidationError(f"'{perm}' is not a valid permission access.")
        return permissions

    @transaction.atomic
    def create(self, validated_data):
        permissions_data = validated_data.pop('permissions')
        post = BlogPost.objects.create(**validated_data)
        self._save_permissions(permissions_data, post)
        return post
    
    @transaction.atomic
    def update(self, instance: BlogPost, validated_data):
        permissions_data = validated_data.pop('permissions')
        instance.title = validated_data.get('title')
        instance.content = validated_data.get('content')
        instance.save()
        self._save_permissions(permissions_data, instance)
        return instance
    
    def _save_permissions(self, permissions_data, post):
        for category, permission in permissions_data.items():
            permissionObj = None
            categoryObj, _ = Category.objects.get_or_create(name=category)
            if permission is not None:
                permissionObj, _ = Permission.objects.get_or_create(name=permission)               
            PostPermission.objects.update_or_create(category=categoryObj, post=post, defaults={'permission':permissionObj})