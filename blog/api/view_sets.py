from rest_framework.request import Request
from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.parsers import JSONParser

from .serializers import BlogPostCreateSerializer

class BlogPostViewSet(viewsets.GenericViewSet):
    parser_classes = (JSONParser,)

    def create(self, request):
        data = request.data
        user = request.user
        data.update({'author': user.id})
        post_serializer = BlogPostCreateSerializer(data=data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status=HTTP_201_CREATED)
        return Response(post_serializer.errors, status=HTTP_400_BAD_REQUEST)