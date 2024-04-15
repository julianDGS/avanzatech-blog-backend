from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist 
from rest_framework import serializers

from ..models import BlogPost
from permission.models import PostPermission, Category, Permission, CategoryName
from user.serializers import ListUserSerializer

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'content', 'author')

    def to_representation(self, instance: BlogPost):
        return {
            'title': instance.title,
            'content': instance.content,
            'excerpt': instance.excerpt,
            'author': {'id': instance.author.id, 'nickname': instance.author.nickname, 'email': instance.author.email},
            'permissions': {cat_perm.category.name: cat_perm.permission.name for cat_perm in instance.reverse_post.all()}
        }
        
class PostPermissionSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    permission_id = serializers.IntegerField()

class BlogPostCreateSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(child=PostPermissionSerializer(), write_only=True, required=True)

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'content', 'author', 'permissions')


    def validate_permissions(self, permissions: list):
        allowed_categories = [choice for choice, _ in CategoryName.choices]
        # allowed_category_ids = [category.id for category in Category.objects.all()]
        # allowed_perm_ids = [permission.id for permission in Permission.objects.all()]
        set_categories = set([permission['category_id'] for permission in permissions])
        if len(set_categories) != len(allowed_categories):
            raise serializers.ValidationError("Missing permission for some category.")
        # for permission_dict in permissions:
        #     if permission_dict['category_id'] not in allowed_category_ids:
        #         raise serializers.ValidationError("There is an illegal category.")
        #     if permission_dict['permission_id'] not in allowed_perm_ids:
        #         raise serializers.ValidationError("There is an illegal permission access.")
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
        for permission_dict in permissions_data:
            try:    
                categoryObj = Category.objects.get(pk=permission_dict['category_id'])
                permissionObj = Permission.objects.get(pk=permission_dict['permission_id'])
            except ObjectDoesNotExist as err:
                raise serializers.ValidationError({'permissions': [err]})
            PostPermission.objects.update_or_create(category=categoryObj, post=post, defaults={'permission':permissionObj})


# class PostPermissionNameSerializer(serializers.Serializer):
#     category = serializers.CharField()
#     permission = serializers.CharField()

# class GroupedPostSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     content = serializers.CharField()
#     author = ListUserSerializer()
#     permissions = PostPermissionNameSerializer()

# def serializer_customized_to_return_post(queryset):
#     grouped_data = []
#     post_perm: PostPermission = None
#     for index in range(len(queryset)):
#         post_perm = queryset[index]
#         id = post_perm.post.id
#         title = post_perm.post.title
#         content = post_perm.post.content
#         author = post_perm.post.author
#         category = post_perm.category.name
#         permission = post_perm.permission.name
#         if index != 0:
#             previous: PostPermission = queryset[index-1]
#             if id == previous.id:
#                 post_perm['permissions'].update(
#                     {category: permission}
#                 )
#             else:
#                 grouped_data.append({
#                     'id': id,
#                     'title': title,
#                     'content': content,
#                     'author': author,
#                     'permissions': {
#                         category: permission
#                     }
#                 })
#         else:
#             grouped_data.append({
#                     'id': id,
#                     'title': title,
#                     'content': content,
#                     'author': author,
#                     'permissions': {
#                         category: permission
#                     }
#                 })
    
#     return grouped_data