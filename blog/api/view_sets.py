from django.db.models import Q
from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.parsers import JSONParser
from rest_framework.decorators import permission_classes

from blog.models import BlogPost

from .serializers import BlogPostCreateSerializer, BlogPostSerializer
from ..pagination import BlogPostPagination
from permission.permissions import AuthenticateAndPostEdit
from permission.models import CategoryName, PermissionName

class BlogPostViewSet(viewsets.GenericViewSet):
    serializer_class = BlogPostSerializer
    parser_classes = (JSONParser,)
    permission_classes = [AuthenticateAndPostEdit]
    # pagination_class = BlogPostPagination

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        return self.get_serializer().Meta.model.objects.filter(id=pk).first()
    
    def _get_list_public_queryset(self):
        global_filter = Q(
                Q(reverse_post__category__name=CategoryName.PUBLIC) &
                ~Q(reverse_post__permission__name=PermissionName.NONE)
            )
        all_data = BlogPost.objects.prefetch_related('reverse_post__category', 'reverse_post__permission', 'author').all()
        queryset = all_data.filter(global_filter)
        return queryset

    def _get_list_queryset(self, user):
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
        global_filter = filter_author | filter_team | filter_authenticate
        all_data = BlogPost.objects.prefetch_related('reverse_post__category', 'reverse_post__permission', 'author').all()
        queryset = all_data.filter(global_filter)
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
        if not user.is_authenticated:
            posts = self._get_list_public_queryset()
        elif user.is_admin:
            posts = self.get_queryset()
        else:
            posts = self._get_list_queryset(user)
        post_serializer = self.get_serializer(posts, many=True)
        return Response(post_serializer.data, status=HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        post = self.get_queryset(pk)
        if post:
            self.check_object_permissions(request, post)
            post_serializer = self.get_serializer(post)
            return Response(post_serializer.data, status=HTTP_200_OK)
        return Response(post_serializer.data, status=HTTP_404_NOT_FOUND)