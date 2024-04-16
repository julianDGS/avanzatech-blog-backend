from django.db.models import Q
from django.contrib.auth.models import AnonymousUser

from permission.models import CategoryName, PermissionName


class ListQuerysetMixin:

    def __get_list_queryset(self, user, reverse_attr=""):
        if isinstance(user, AnonymousUser):
            return Q(
                Q(**{f'{reverse_attr}reverse_post__category__name': CategoryName.PUBLIC}) &
                ~Q(**{f'{reverse_attr}reverse_post__permission__name': PermissionName.NONE})
            )
        elif user.is_admin:
            return None
        else:
            filter_author = Q(
                Q(**{f'{reverse_attr}author_id' : user.id}) & 
                Q(**{f'{reverse_attr}reverse_post__category__name' : CategoryName.AUTHOR}) &
                ~Q(**{f'{reverse_attr}reverse_post__permission__name' : PermissionName.NONE})
            )
            filter_team = Q(
                ~Q(**{f'{reverse_attr}author_id' : user.id}) &
                Q(**{f'{reverse_attr}author__team_id' : user.team.id}) &
                Q(**{f'{reverse_attr}reverse_post__category__name' : CategoryName.TEAM}) &
                ~Q(**{f'{reverse_attr}reverse_post__permission__name' : PermissionName.NONE})
            )
            filter_authenticate = Q(
                ~Q(**{f'{reverse_attr}author_id' : user.id}) &
                ~Q(**{f'{reverse_attr}author__team_id' : user.team.id}) &
                Q(**{f'{reverse_attr}reverse_post__category__name' : CategoryName.AUTHENTICATE}) &
                ~Q(**{f'{reverse_attr}reverse_post__permission__name' : PermissionName.NONE})
            )
            return filter_author | filter_team | filter_authenticate           

    def get_post_list(self, user, model):
        global_filter = self.__get_list_queryset(user)
        all_data = model.objects.prefetch_related('reverse_post__category', 'reverse_post__permission', 'author').all()
        if not global_filter:
            return all_data.order_by('-created_at')    
        return all_data.filter(global_filter).order_by('-created_at')
    
    def get_like_list(self, user, model, reverse_attr):
        global_filter = self.__get_list_queryset(user, reverse_attr)
        all_data = model.objects.prefetch_related(f'{reverse_attr}reverse_post__category', f'{reverse_attr}reverse_post__permission', f'{reverse_attr}author').all()
        if not global_filter:
            return all_data.order_by('-created_at')    
        return all_data.filter(global_filter).order_by('-created_at')