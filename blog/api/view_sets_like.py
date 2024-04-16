from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.status import *

from django_filters.rest_framework import DjangoFilterBackend

from blog.api.serializers_like import LikeSerializer
from blog.models import BlogPost

from permission.permissions import AuthenticateAndLikePermission

class LikeViewSet(viewsets.GenericViewSet):
    serializer_class = LikeSerializer
    parser_classes = (JSONParser,)
    permission_classes = [AuthenticateAndLikePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'user']

    def get_queryset(self, post_filter=None):
        if post_filter:
            return self.get_serializer().Meta.model.objects.prefetch_related('post', 'user').filter()
        return self.get_serializer().Meta.model.objects.prefetch_related('post', 'user').all()

    def create(self, request):
        post = BlogPost.objects.filter(pk=request.data['post_id']).first()
        if post:
            self.check_object_permissions(request, post)
            user = request.user
            data = {'post': post.id, 'user': user.id}
            like_serializer = LikeSerializer(data=data)
            if like_serializer.is_valid():
                like_serializer.save()
                return Response(like_serializer.data, status=HTTP_201_CREATED)
            return Response(like_serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response({'error': 'Post not found.'}, status=HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        post = BlogPost.objects.filter(pk=pk).first()
        if post:
            like = self.get_serializer().Meta.model.objects.filter(post_id=post.id, user_id=request.user.id)
            if like:
                self.check_object_permissions(request, post)
                like.delete()
                return Response({'message', f'Like from {request.user.nickname} deleted.'}, status=HTTP_204_NO_CONTENT)
        return Response({'error': 'Post not found.'}, status=HTTP_404_NOT_FOUND)
    
    # def list(self, request):
    #     post_filter = self.request.query_params.get('post')
    #     if post_filter:
    #         queryset = self.get_queryset(post_filter)
    #         queryset = self.filter_queryset(queryset)
    #         import pdb; pdb.set_trace()
    #         # page = self.paginate_queryset(queryset)
    #         # if page is not None:
    #         #     likes_serializer = self.get_serializer(page, many=True)
    #         #     return self.get_paginated_response(likes_serializer.data)
    #         likes_serializer = self.get_serializer(queryset, many=True)
    #         return Response(likes_serializer.data, status=HTTP_200_OK)
    #     return Response({'error': 'post param is required'}, HTTP_400_BAD_REQUEST)
