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