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


    def validate(self, data: dict):
        super().validate(data)
        permissions = data.get('permissions')
        allowed_categories = [choice for choice, name in CategoryName.choices]
        allowed_perms = [choice for choice, name in PermissionName.choices] + [None]
        if len(permissions) != len(allowed_categories):
            raise serializers.ValidationError(f"Missing permission for some category.")
        for category, perm in permissions.items():
            if category not in allowed_categories:
                raise serializers.ValidationError(f"'{category}' is not a valid category.")
            if perm not in allowed_perms:
                raise serializers.ValidationError(f"'{category}' is not a valid permission access.")
        return data

    def create(self, validated_data):
        permissions_data = validated_data.pop('permissions')
        post = BlogPost.objects.create(**validated_data)
        for category, permission in permissions_data.items():
            permissionObj = None
            categoryObj, _ = Category.objects.get_or_create(name=category)
            if permission is not None:
                permissionObj, _ = Permission.objects.get_or_create(name=permission)               
            permission = PostPermission.objects.create(category=categoryObj, permission=permissionObj, post=post)
        return post