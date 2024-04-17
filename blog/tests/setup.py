from django.urls import reverse
from rest_framework.test import APITestCase

from permission.models import Category, Permission, CategoryName, PermissionName
from user.tests.factories.user_factories import TeamFactory, UserFactory
from .factories.blog_post_factories import BlogPostFactory


class AuthenticateSetUp(APITestCase):

        def setUp(self):
            login_url = reverse('login')
            self.post_url = '/post/'
            self.like_url = '/like/'

            self.user = UserFactory(email="user@mail.com", set_user_password="223344")
            
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

            self.post_author = BlogPostFactory(author=self.user)
            self.post_team = BlogPostFactory(author=UserFactory(team=self.user.team))
            self.post_authenticate = BlogPostFactory(author=UserFactory(team=TeamFactory(name='other team')))