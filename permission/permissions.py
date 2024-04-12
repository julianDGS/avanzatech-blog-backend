from rest_framework.permissions import BasePermission, SAFE_METHODS

from user.models import User
from .models import CategoryName, PermissionName, PostPermission

class AuthenticateAndPostEdit(BasePermission):
    
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['HEAD', 'OPTIONS']:
            return True
        user: User = request.user
        author: User = User.objects.get(id=obj.author.id)
        post_permissions = PostPermission.objects.filter(post_id=obj.id)
        post_permissions_dict = {permission.category.name: permission.permission.name for permission in post_permissions}
        if request.method == 'GET':
            if user.is_admin:
                return True
            if user.id == author.id:
                if post_permissions_dict[str(CategoryName.AUTHOR)] != str(PermissionName.NONE):
                    return True
                else:
                    return False
            if user.team.id == author.team.id:
                if post_permissions_dict[str(CategoryName.TEAM)] != str(PermissionName.NONE):
                    return True
                else:
                    return False
            if post_permissions_dict[str(CategoryName.AUTHENTICATE)] != str(PermissionName.NONE):
                return True
        else:      
            if user.is_admin:
                return True
            if user.id == author.id:
                if post_permissions_dict[str(CategoryName.AUTHOR)] == str(PermissionName.EDIT):
                    return True
                else:
                    return False
            if user.team.id == author.team.id:
                if post_permissions_dict[str(CategoryName.TEAM)] == str(PermissionName.EDIT):
                    return True
                else:
                    return False
            if post_permissions_dict[str(CategoryName.AUTHENTICATE)] == str(PermissionName.EDIT):
                return True
        return False
