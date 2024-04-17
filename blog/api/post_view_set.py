from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.parsers import JSONParser


from blog.models import BlogPost

from .post_serializers import BlogPostCreateSerializer, BlogPostSerializer
from mixins.pagination_mixin import BlogPostPagination
from permission.permissions import AuthenticateAndPostEdit
from mixins.queryset_mixin import ListQuerysetMixin


class BlogPostViewSet(viewsets.GenericViewSet, ListQuerysetMixin):
    serializer_class = BlogPostSerializer
    parser_classes = (JSONParser,)
    permission_classes = [AuthenticateAndPostEdit]
    pagination_class = BlogPostPagination


    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all().order_by('-created_at')
        return self.get_serializer().Meta.model.objects.prefetch_related('reverse_post__category', 'reverse_post__permission', 'author').filter(id=pk).first()


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
            data.update({'author': post.author.id})
            post_serializer = BlogPostCreateSerializer(post, data=data)
            if post_serializer.is_valid():
                post_serializer.save()
                return Response(post_serializer.data, status=HTTP_200_OK)
            return Response(post_serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response({'error': 'Post not found.'}, status=HTTP_404_NOT_FOUND)
    

    def list(self, request):
        user = request.user
        posts = self.list_queryset(user, BlogPost)
        page = self.paginate_queryset(self.filter_queryset(posts))
        if page is not None:
            post_serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(post_serializer.data)
        post_serializer = self.get_serializer(posts, many=True)
        return Response(post_serializer.data, status=HTTP_200_OK)
    

    def retrieve(self, request, pk=None):
        post = self.get_queryset(pk)
        if post:
            self.check_object_permissions(request, post)
            post_serializer = self.get_serializer(post)
            return Response(post_serializer.data, status=HTTP_200_OK)
        return Response(post_serializer.data, status=HTTP_404_NOT_FOUND)