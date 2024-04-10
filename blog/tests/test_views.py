from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework.status import *

from ..models import BlogPost
from user.models import User
from permission.models import PostPermission, Category, Permission, CategoryName, PermissionName
from .factories.blog_post_factories import BlogPostFactory
from permission.tests.factories.permission_factories import PostWithPermissionFactory

class BlogPostWithAuthenticationTest(APITestCase):
    
    def setUp(self):
        login_url = reverse('login')
        self.post_url = '/post/'
        self.user = User.objects.create_user(email="admin2@mail.com", password="223344")
        
        self.public = Category.objects.create(name=CategoryName.PUBLIC)
        self.auth = Category.objects.create(name=CategoryName.AUTHENTICATE)
        self.team = Category.objects.create(name=CategoryName.TEAM)
        self.author = Category.objects.create(name=CategoryName.AUTHOR)
        self.read = Permission.objects.create(name=PermissionName.READ)
        self.edit = Permission.objects.create(name=PermissionName.EDIT)
        self.none = Permission.objects.create(name=PermissionName.NONE)
        
        self.data = {
            'title': 'Leave sense plan.', 
            'content': 'Effect somebody drug figure quality success. There government work commercial. Good various prevent suddenly. Concern create relationship. Want moment accept kitchen gun. Day popular generation bring stage.', 
            'permissions': [
                {"category_id": self.public.id, "permission_id": self.none.id},
                {"category_id": self.auth.id, "permission_id": self.read.id},
                {"category_id": self.team.id, "permission_id": self.edit.id},
                {"category_id": self.author.id, "permission_id": self.edit.id}
            ]
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
        categories = [self.public, self.auth, self.team, self.author]
        self.assertTrue(all(permission.category in categories for permission in permissions))

    def test_view_can_handle_post_with_missing_fields(self):
        test_data = [
            {**self.data, 'title': None},
            {**self.data, 'content': None},
            {**self.data, 'permissions': [
                {'category_id': self.auth.id, 'permission_id': self.read.id}, 
                {'category_id': self.author.id, 'permission_id': self.read.id}, 
                {'category_id': self.team.id, 'permission_id': self.read.id}
            ]},
            {**self.data, 'permissions': [
                {'category_id': self.public.id, 'permission_id': self.read.id}, 
                {'category_id': self.author.id, 'permission_id': self.read.id}, 
                {'category_id': self.team.id, 'permission_id': self.read.id}
            ]},
            {**self.data, 'permissions': [
                {'category_id': self.public.id, 'permission_id': self.read.id}, 
                {'category_id': self.auth.id, 'permission_id': self.read.id}, 
                {'category_id': self.team.id, 'permission_id': self.read.id}
            ]},
            {**self.data, 'permissions': [
                {'category_id': self.public.id, 'permission_id': self.read.id}, 
                {'category_id': self.auth.id, 'permission_id': self.read.id}, 
                {'category_id': self.author.id, 'permission_id': self.read.id}
            ]},
        ]

        for data in test_data:    
            with self.subTest(data=data):
                response: Response = self.client.post(self.post_url, data, format='json')
                self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_view_can_handle_post_with_wrong_permission_category(self):
        data = {**self.data, 'permissions': [
                        {'category_id': self.public.id, 'permission_id': self.read.id}, 
                        {'category_id': self.auth.id, 'permission_id': self.read.id},
                        {'category_id': self.team.id, 'permission_id': self.read.id},
                        {'category_id': -1, 'permission_id': self.read.id}
                    ]
                }
        response: Response = self.client.post(self.post_url, data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['permissions'][0], "There is an illegal category.")

    def test_view_can_handle_post_with_wrong_permission_assigned_to_category(self):
        data = {**self.data, 'permissions': [
                        {'category_id': self.public.id, 'permission_id': self.read.id}, 
                        {'category_id': self.auth.id, 'permission_id': self.read.id},
                        {'category_id': self.team.id, 'permission_id': self.read.id},
                        {'category_id': self.author.id, 'permission_id': -1}
                    ]
                }
        response: Response = self.client.post(self.post_url, data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['permissions'][0], "There is an illegal permission access.")
    
    def test_view_can_handle_post_with_duplicate_permission_categories(self):
        data = {**self.data, 'permissions': [
                        {'category_id': self.public.id, 'permission_id': self.read.id}, 
                        {'category_id': self.public.id, 'permission_id': self.read.id},
                        {'category_id': self.team.id, 'permission_id': self.read.id},
                        {'category_id': self.team.id, 'permission_id': self.read.id}
                    ]
                }
        response: Response = self.client.post(self.post_url, data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['permissions'][0], "Missing permission for some category.")

    def test_view_updates_post_data(self):
        post = BlogPostFactory(author=self.user)
        # Since CategoryFactory and PermissionFactory has Iterator and it gets value in order, create a batch of 4 elements will contain all permissions
        PostWithPermissionFactory.create_batch(4, post=post)
        permissions = PostPermission.objects.all()
        self.assertTrue(len(permissions), 4)
        self.assertEqual(permissions[0].permission.name, 'read')
        self.assertEqual(permissions[1].permission.name, 'edit')
        self.assertEqual(permissions[2].permission.name, 'none')
        self.assertEqual(permissions[3].permission.name, 'read')

        response: Response = self.client.put(f'{self.post_url}{post.id}/', self.data, format='json')
        permissions = PostPermission.objects.all()
        self.assertTrue(len(permissions), 4)
        self.assertEqual(response.data['id'], post.id)
        self.assertDictEqual(
            {permission.category.id: permission.permission.id for permission in permissions}, 
            {permission['category_id']: permission['permission_id'] for permission in self.data['permissions']}
        )
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


