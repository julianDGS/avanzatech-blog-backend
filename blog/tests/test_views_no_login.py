from rest_framework.test import APITestCase
from rest_framework.status import *

from blog.tests.factories.blog_post_factories import BlogPostFactory
from permission.models import Category, CategoryName, Permission, PermissionName, PostPermission
from permission.tests.factories.permission_factories import PostWithPermissionFactory
from ..models import BlogPost
from user.models import User

class BlogPostWithNoAuthTest(APITestCase):

    def setUp(self):
        self.post_url = '/post/'
        self.user = User.objects.create_user(email="admin2@mail.com", password="223344")
        public = Category.objects.create(name=CategoryName.PUBLIC)
        auth = Category.objects.create(name=CategoryName.AUTHENTICATE)
        team = Category.objects.create(name=CategoryName.TEAM)
        author = Category.objects.create(name=CategoryName.AUTHOR)
        read = Permission.objects.create(name=PermissionName.READ)
        edit = Permission.objects.create(name=PermissionName.EDIT)
        none = Permission.objects.create(name=PermissionName.NONE)
        self.data = {
            'title': 'Leave sense plan.', 
            'content': 'Effect somebody drug figure quality success. There government work commercial.',
            'permissions': [
                {"category_id": public.id, "permission_id": none.id},
                {"category_id": auth.id, "permission_id": read.id},
                {"category_id": team.id, "permission_id": edit.id},
                {"category_id": author.id, "permission_id": edit.id}
            ]
        }

    def test_view_does_not_create_post_with_no_auth_user(self): 
        response = self.client.post(self.post_url, self.data, format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertFalse(BlogPost.objects.all())
        self.assertFalse(PostPermission.objects.all())

    def test_view_does_not_update_post_with_no_auth_user(self):
        post = BlogPostFactory(author=self.user)
        # Since CategoryFactory and PermissionFactory has Iterator and it gets value in order, create a batch of 4 elements will contain all permissions
        PostWithPermissionFactory.create_batch(4, post=post)
        response = self.client.put(f'{self.post_url}{post.id}/', self.data, format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_view_shows_correct_posts_with_no_auth_user(self):
        pass