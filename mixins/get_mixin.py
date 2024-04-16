from django.db.models import Q
from django.contrib.auth.models import AnonymousUser

from permission.models import CategoryName, PermissionName


class ListQuerysetMixin:

    def __get_list_queryset(self, user):
        if isinstance(user, AnonymousUser):
            return Q(
                Q(reverse_post__category__name=CategoryName.PUBLIC) &
                ~Q(reverse_post__permission__name=PermissionName.NONE)
            )
        elif user.is_admin:
            return None
        else:
            filter_author = Q(
                Q(author_id=user.id) & 
                Q(reverse_post__category__name=CategoryName.AUTHOR) &
                ~Q(reverse_post__permission__name=PermissionName.NONE)
            )
            filter_team = Q(
                ~Q(author_id=user.id) &
                Q(author__team_id=user.team.id) &
                Q(reverse_post__category__name=CategoryName.TEAM) &
                ~Q(reverse_post__permission__name=PermissionName.NONE)
            )
            filter_authenticate = Q(
                ~Q(author_id=user.id) &
                ~Q(author__team_id=user.team.id) &
                Q(reverse_post__category__name=CategoryName.AUTHENTICATE) &
                ~Q(reverse_post__permission__name=PermissionName.NONE)
            )
            return filter_author | filter_team | filter_authenticate           

    def get_post_list(self, user, model):
        global_filter = self.__get_list_queryset(user)
        all_data = model.objects.prefetch_related('reverse_post__category', 'reverse_post__permission', 'author').all()
        if not global_filter:
            return all_data.order_by('-created_at')    
        return all_data.filter(global_filter).order_by('-created_at')
    
    def get_like_list(self, user, model):
        global_filter = self.__get_list_queryset(user)
        all_data = model.objects.prefetch_related('post__reverse_post__category', 'post__reverse_post__permission', 'post__author').all()
        if not global_filter:
            return all_data.order_by('-created_at')    
        return all_data.filter(global_filter).order_by('-created_at')