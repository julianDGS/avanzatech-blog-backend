from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist 
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from ..models import BlogPost
from permission.models import PostPermission, Category, Permission, CategoryName

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'content', 'author')

    def to_representation(self, instance: BlogPost):
        response = {
            'id': instance.id,
            'title': instance.title,
            'content': instance.content,
            'content_html': instance.content_html,
            'excerpt': instance.excerpt,
            'createdAt': instance.created_at,
            'author': {
                'id': instance.author.id, 
                'nickname': instance.author.nickname, 
                'email': instance.author.email, 
                'team': {
                  'id': instance.author.team.id,
                  'name': instance.author.team.name  
                } 
            },
            'permissions': {
                cat_perm.category.name: {'id':cat_perm.permission.id, 'name':cat_perm.permission.name} for cat_perm in instance.reverse_post.all()
            },
            'likes': instance.likes.count(),
            'comments': instance.comments.count()
        }
        user = self.context.get('request').user
        if not isinstance(user, AnonymousUser):
            like_count = instance.likes.filter(id=user.id).count()
            response['post_liked'] = True if like_count > 0 else False;
        return response
        
class PostPermissionSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    permission_id = serializers.IntegerField()

class BlogPostCreateSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(child=PostPermissionSerializer(), write_only=True, required=True)

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'content', 'author', 'permissions', 'content_html')


    def validate_permissions(self, permissions: list):
        allowed_categories = [choice for choice, _ in CategoryName.choices]
        set_categories = set([permission['category_id'] for permission in permissions])
        if len(set_categories) != len(allowed_categories):
            raise serializers.ValidationError("Missing permission for some category.")
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
        instance.content = validated_data.get('content_html')
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

