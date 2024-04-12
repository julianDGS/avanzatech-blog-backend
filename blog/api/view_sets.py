from django.db.models import Q
from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.parsers import JSONParser

from rest_framework.permissions import IsAuthenticated

from .serializers import BlogPostCreateSerializer, BlogPostSerializer
from ..pagination import BlogPostPagination
from permission.permissions import AuthenticateAndPostEdit
from permission.models import PostPermission, CategoryName, PermissionName

class BlogPostViewSet(viewsets.GenericViewSet):
    serializer_class = BlogPostSerializer
    parser_classes = (JSONParser,)
    permission_classes = [AuthenticateAndPostEdit]
    # pagination_class = BlogPostPagination

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        return self.get_serializer().Meta.model.objects.filter(id=pk).first()
    
    def _get_list_queryset(self, user):
        filter_author = Q(
            Q(post__author_id=user.id) & 
            Q(category__name=CategoryName.AUTHOR) &
            ~Q(permission__name=PermissionName.NONE)
        )
        filter_team = Q(
            ~Q(post__author_id=user.id) &
            Q(post__author__team_id=user.team.id) &
            Q(category__name=CategoryName.TEAM) &
            ~Q(permission__name=PermissionName.NONE)
        )
        filter_authenticate = Q(
            ~Q(post__author_id=user.id) &
            ~Q(post__author__team_id=user.team.id) &
            Q(category__name=CategoryName.AUTHENTICATE) &
            ~Q(permission__name=PermissionName.NONE)
        )
        all_data = PostPermission.objects.prefetch_related('post', 'category', 'permission').all()
        queryset = all_data.filter(filter_author | filter_team | filter_authenticate)
        return queryset

    def create(self, request):
        data = request.data
        user = request.user
        data.update({'author': user.id})
        post_serializer = BlogPostCreateSerializer(data=data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status=HTTP_201_CREATED)
        return Response(post_serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        post = self.get_queryset(pk)
        if post:
            self.check_object_permissions(request, post)
            data = request.data
            user = request.user
            data.update({'author': user.id})
            post_serializer = BlogPostCreateSerializer(post, data=data)
            if post_serializer.is_valid():
                post_serializer.save()
                return Response(post_serializer.data, status=HTTP_200_OK)
            return Response(post_serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response({'error': 'Post not found.'}, status=HTTP_404_NOT_FOUND)
    
    def list(self, request):
        user = request.user
        posts = None
        if user.is_admin:
            posts = self.get_queryset()
        else:
            queryset = self._get_list_queryset(user)
            posts = [permission.post for permission in queryset]
        post_serializer = self.get_serializer(posts, many=True)
        return Response(post_serializer.data, status=HTTP_200_OK)