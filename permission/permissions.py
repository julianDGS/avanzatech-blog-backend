from rest_framework.permissions import BasePermission, SAFE_METHODS

from user.models import User
from .models import CategoryName, PermissionName, PostPermission

class AuthenticateAndPostEdit(BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user: User = request.user
        author: User = User.objects.get(id=obj.author.id)
        # import pdb; pdb.set_trace()
        if user.is_admin:
            return True
        post_permissions = PostPermission.objects.filter(post_id=obj.id)
        post_permissions_dict = {permission.category.name: permission.permission.name for permission in post_permissions}
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
