from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework.status import *

from permission.models import PostPermission
from ..models import BlogPost
from user.models import User
from .factories.blog_post_factories import BlogPostFactory
from permission.tests.factories.permission_factories import PostWithPermissionFactory

class BlogPostWithAuthenticationTest(APITestCase):
    
    def setUp(self):
        login_url = reverse('login')
        self.post_url = '/post/'
        self.user = User.objects.create_user(email="admin2@mail.com", password="223344")
        self.data = {
            'title': 'Leave sense plan.', 
            'content': 'Effect somebody drug figure quality success. There government work commercial. Good various prevent suddenly. Concern create relationship. Want moment accept kitchen gun. Day popular generation bring stage.', 
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

    def test_view_assigns_author_from_logged_user(self):
        response = self.client.post(self.post_url, self.data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertTrue(response.data['author'])
        self.assertTrue(response.data['id'])
        self.assertTrue(BlogPost.objects.first())

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
        test_data = [
            {**self.data, 'title': None},
            {**self.data, 'content': None},
            {**self.data, 'permissions': {'auth': 'read', 'author': 'read', 'team': 'read'}},
            {**self.data, 'permissions': {'public': 'read', 'author': 'read', 'team': 'read'}},
            {**self.data, 'permissions': {'public': 'read', 'auth': 'read', 'team': 'read'}},
            {**self.data, 'permissions': {'public': 'read', 'auth': 'read', 'author': 'read'}},
        ]

        for data in test_data:    
            with self.subTest(data=data):
                response: Response = self.client.post(self.post_url, data, format='json')
                self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_view_can_handle_post_with_wrong_permission_category(self):
        data = {**self.data, 'permissions': {'public': 'read', 'auth': 'read', 'author': 'read', 'team-wrong': 'read'}}
        response: Response = self.client.post(self.post_url, data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['permissions'][0], "'team-wrong' is not a valid category.")

    def test_view_can_handle_post_with_wrong_permission_assigned_to_category(self):
        data = {**self.data, 'permissions': {'public': 'read', 'auth': 'read', 'author': 'read', 'team': 'read-wrong'}}
        response: Response = self.client.post(self.post_url, data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['permissions'][0], "'read-wrong' is not a valid permission access.")

    def test_view_updates_post_data(self):
        post = BlogPostFactory(author=self.user)
        # Since CategoryFactory and PermissionFactory has Iterator and it gets value in order, create a batch of 4 elements will contain all permissions
        PostWithPermissionFactory.create_batch(4, post=post)
        permissions = PostPermission.objects.all()
        self.assertTrue(len(permissions), 4)
        categories = ['public', 'auth', 'team', 'author']
        self.assertTrue(all(permission.category.name in categories for permission in permissions))
        self.assertEqual(permissions[0].permission.name, 'read')
        self.assertEqual(permissions[1].permission.name, 'edit')
        self.assertEqual(permissions[2].permission.name, 'read')
        self.assertEqual(permissions[3].permission.name, 'edit')

        response: Response = self.client.put(f'{self.post_url}{post.id}/', self.data, format='json')
        permissions = PostPermission.objects.all()
        # self.assertEqual(response.data['permissions']['public'], 'read')
        # self.assertEqual(response.data['permissions']['auth'], None)
        # self.assertEqual(response.data['permissions']['team'], 'edit')
        # self.assertEqual(response.data['permissions']['author'], 'read')
        self.assertTrue(len(permissions), 4)
        self.assertEqual(response.data['id'], post.id)
        self.assertDictEqual({permission.category.name: (permission.permission.name if permission.permission else None) for permission in permissions}, self.data['permissions'])
        self.assertEqual(response.data['title'], self.data['title'])
        self.assertEqual(response.data['content'], self.data['content'])

    def test_view_updates_post_permissions(self):
        pass

    def test_view_can_handle_wrong_data_on_update(self):
        pass

    def test_view_updates_only_necesary_fields(self):
        pass

    def test_view_does_not_update_post_with_no_edit_permissions(self):
        pass

    def test_view_shows_correct_posts_with_user_as_author(self):
        pass

    def test_view_shows_correct_posts_with_user_as_team_member(self):
        pass

    def test_view_shows_correct_posts_with_user_as_authenticated(self):
        pass


