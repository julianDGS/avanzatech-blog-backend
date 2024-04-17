from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.status import *

from django_filters.rest_framework import DjangoFilterBackend

from blog.api.comment_serializers import CommentSerializer
from blog.models import BlogPost
from mixins.queryset_mixin import ListQuerysetMixin
from permission.permissions import AuthenticateAndCommentPermission

class CommentViewSet(viewsets.GenericViewSet, ListQuerysetMixin):
    pass
    serializer_class = CommentSerializer
    parser_classes = (JSONParser,)
    permission_classes = [AuthenticateAndCommentPermission]


    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.prefetch_related('post', 'user').all()


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
        post = BlogPost.objects.filter(pk=pk).first()
        if post:
            comment = self.get_serializer().Meta.model.objects.filter(post_id=post.id, user_id=request.user.id)
            if comment:
                self.check_object_permissions(request, post)
                comment.delete()
                return Response({'message', f'Comment from {request.user.nickname} deleted.'}, status=HTTP_204_NO_CONTENT)
        return Response({'error': 'Post not found.'}, status=HTTP_404_NOT_FOUND)

