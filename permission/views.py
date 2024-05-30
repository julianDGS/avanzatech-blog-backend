from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.generics import ListAPIView

from .serializers import PermissionSerializer, CategorySerializer


class PermissionView(ListAPIView):
    serializer_class=PermissionSerializer
    
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()

class CategoryView(ListAPIView):
    serializer_class=CategorySerializer
    
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()