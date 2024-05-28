from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.status import *

from django_filters.rest_framework import DjangoFilterBackend

from blog.api.comment_serializers import CommentSerializer
from blog.models import BlogPost, Comment
from mixins.pagination_mixin import CommentPagination
from mixins.queryset_mixin import ListQuerysetMixin
from permission.permissions import AuthenticateAndCommentPermission

class CommentViewSet(viewsets.GenericViewSet, ListQuerysetMixin):
    pass
    serializer_class = CommentSerializer
    parser_classes = (JSONParser,)
    permission_classes = [AuthenticateAndCommentPermission]
    pagination_class = CommentPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'user']


    def create(self, request):
        post = BlogPost.objects.filter(pk=request.data['post_id']).first()
        if post:
            self.check_object_permissions(request, post)
            user = request.user
            data = {'post': post.id, 'user': user.id, 'comment': request.data['comment']}
            like_serializer = CommentSerializer(data=data)
            if like_serializer.is_valid():
                like_serializer.save()
                return Response(like_serializer.data, status=HTTP_201_CREATED)
            return Response(like_serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response({'error': 'Post not found.'}, status=HTTP_404_NOT_FOUND)
    

    def destroy(self, request, pk=None):
        comment = self.get_serializer().Meta.model.objects.filter(pk=pk).first()        
        if comment:
            if comment.user.id == request.user.id:
                self.check_object_permissions(request, comment.post)
                comment.delete()
                return Response(status=HTTP_204_NO_CONTENT)
            return Response({'error': 'You have not commented this post.'}, status=HTTP_400_BAD_REQUEST)
        return Response({'error': 'Comment not found.'}, status=HTTP_404_NOT_FOUND)


    def list(self, request):
        queryset = self.list_queryset(request.user, Comment, 'post__')
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        likes_serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(likes_serializer.data)
