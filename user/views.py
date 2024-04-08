from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import *

from .serializers import ListUserSerializer, UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request: Request):
    username = request.data.get('username', '')
    password = request.data.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        user_serializer = ListUserSerializer(user)
        return Response(
            {
                'message': 'Successful Login',
                'user': user_serializer.data
            },
            status=HTTP_200_OK
        )
    else:
        # Return an 'invalid login' error message.
        return Response({'error': 'Invalid credentials'}, status=HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Successful Logout'}, status=HTTP_200_OK)

@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    data = request.data
    user_serializer = UserSerializer(data=data)
    if user_serializer.is_valid():
        user_serializer.save() 
        return Response(user_serializer.data, status=HTTP_201_CREATED)
        
    return Response(user_serializer.errors, status=HTTP_400_BAD_REQUEST)