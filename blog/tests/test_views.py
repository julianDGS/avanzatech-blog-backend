from django.urls import reverse
from django.forms.models import model_to_dict
import json.scanner
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework.status import *

import json
from ..models import User
from .factories.blog_post_factories import * 
from permission.tests.factories.permission_factories import *

class BlogPostWithAuthenticationTest(APITestCase):
    
    def setUp(self):
        login_url = reverse('login')
        self.post_url = '/post/'
        self.user = User.objects.create_user(email="admin2@mail.com", password="223344")
        self.data = {
            'title': 'Leave sense plan.', 
            'content': 'Effect somebody drug figure quality success. There government work commercial. Good various prevent suddenly. Concern create relationship. Want moment accept kitchen gun. Day popular generation bring stage. Tv hour order away structure admit hand. Go win various. Share price food relationship bit include. However get score movement down stage.', 
            'author': self.user.id, 
            'permissions': {
                'public': 'read', 
                'auth': None, 
                'team': 'edit', 
                'author': 'read'
            }
        }
        self.client.post(
            login_url,
            {
                'username': self.user.email,
                'password': "223344"
            },
            format='json'
        )

    def test_view_creates_post_with_all_permission(self):
        response =  self.client.post(
            self.post_url, 
            self.data,
            format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.data['title'])
        self.assertTrue(response.data['id'])
        self.assertTrue(BlogPost.objects.first())
        
        permissions = PostPermission.objects.all()
        categories = ['public', 'auth', 'team', 'author']
        self.assertTrue(all(permission.category.name in categories for permission in permissions))

    def test_view_can_handle_post_with_missing_fields(self):
        pass

    def test_view_assigns_author_from_logged_user(self):
        pass

    def test_view_can_handle_post_with_missing_permissions(self):
        pass

    def test_view_shows_correct_posts_with_user_as_author(self):
        pass

    def test_view_shows_correct_posts_with_user_as_team_member(self):
        pass

    def test_view_shows_correct_posts_with_user_as_authenticated(self):
        pass


