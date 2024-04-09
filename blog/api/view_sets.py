from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.parsers import JSONParser

from .serializers import BlogPostCreateSerializer, BlogPostSerializer

class BlogPostViewSet(viewsets.GenericViewSet):
    serializer_class = BlogPostSerializer
    parser_classes = (JSONParser,)

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        return self.get_serializer().Meta.model.objects.filter(id=pk).first()

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
            data = request.data
            user = request.user
            data.update({'author': user.id})
            post_serializer = BlogPostCreateSerializer(post, data=data)
            if post_serializer.is_valid():
                post_serializer.save()
                return Response(post_serializer.data, status=HTTP_200_OK)
            return Response(post_serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response({'error': 'Post not found.'}, status=HTTP_404_NOT_FOUND)