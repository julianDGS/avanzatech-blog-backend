from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.contrib.sessions.models import Session
from rest_framework.response import Response
from rest_framework.status import *

from ..models import User
from .factories.user_factories import * 

class UserAuthenticateTest(TestCase):
    
    def test_login(self):
        user = User.objects.create_user(email="admin2@mail.com", password="223344")
        response = self._login_user(user)
        user_resp = { "id":user.id , "email": user.email, "name": user.name, "last_name": user.last_name, "nickname": user.nickname}

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['user'], user_resp)
        
        session = Session.objects.first()
        session_data = session.get_decoded()
        user_id = int(session_data.get('_auth_user_id'))
        self.assertEqual(user.id, user_id)

    def test_login_fail(self):
        login_url = reverse('login')
        user = User.objects.create_user(email="admin2@mail.com", password="223344")

        response: Response = self.client.post(
            login_url,
            {
                'username': user.email,
                'password': '111111'
            },
            format='json'
        )
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertFalse(Session.objects.first())

    def test_logout(self):
        user = User.objects.create_user(email="admin2@mail.com", password="223344")
        self._login_user(user)
        self.assertTrue(Session.objects.first())

        logout_url = reverse('logout')

        response: Response = self.client.get(logout_url, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertFalse(Session.objects.first())

    def test_register_user(self):
        register_url = reverse('register')
        data = {
                'email': "user@mail.com",
                'password': "223344",
                "confirm_password": "223344",
                "name": "first name",
                "last_name": "last name"
        }
        response: Response = self.client.post(register_url, data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['last_name'], data['last_name'])
        self.assertTrue(User.objects.first())

    def test_register_duplicate_user(self):
        User.objects.create(email="user@mail.com", password="223344")
        register_url = reverse('register')
        data = {
                'email': "user@mail.com",
                'password': "223344",
                "confirm_password": "223344",
                "name": "first name",
                "last_name": "last name"
        }
        response: Response = self.client.post(register_url, data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    
    def test_register_user_without_required_fields(self):
        register_url = reverse('register')

        test_data = [
            {'email': "", 'password': "223344", "confirm_password": "223344", "name": "name 1", "last_name": "last name 1"},
            {'email': "user2@mail.com", 'password': "", "name": "name 2", "last_name": "last name 2"}
        ]
        for data in test_data:
            with self.subTest(data=data):
                response = self.client.post(register_url, **data, format='json')
                self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
    
    def test_register_user_ignore_extra_fields_from_serializer(self):
        register_url = reverse('register')
        data = {
            'email': "user@mail.com", 
            'password': "223344", 
            "confirm_password": "223344", 
            "name": "name 1", 
            "last_name": "last name 1", 
            "team": 1
        }
        response = self.client.post(register_url, data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
    
    def test_register_user_with_incorrect_passwords(self):
        register_url = reverse('register')
        data = {
            'email': "user@mail.com", 
            'password': "223344", 
            "confirm_password": "111111", 
            "name": "name 1", 
            "last_name": "last name 1", 
        }
        response = self.client.post(register_url, data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)


    def _login_user(self, user):
        login_url = reverse('login')

        return self.client.post(
            login_url,
            {
                'username': user.email,
                'password': "223344"
            },
            format='json'
        )