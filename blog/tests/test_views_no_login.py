from rest_framework.test import APITestCase
from rest_framework.status import *

from permission.models import PostPermission
from ..models import BlogPost
from user.models import User

class BlogPostWithNoAuthTest(APITestCase):

    def test_view_does_not_create_post_with_no_auth_user(self):
        User.objects.create_user(email="admin2@mail.com", password="223344")
        data = {
            'title': 'Leave sense plan.', 
            'content': 'Effect somebody drug figure quality success. There government work commercial.',
            'permissions': {
                'public': 'read', 
                'auth': None, 
                'team': 'edit', 
                'author': 'read'
            }
        }
        response = self.client.post('/post/', data, format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertFalse(BlogPost.objects.all())
        self.assertFalse(PostPermission.objects.all())

    def test_view_shows_correct_posts_with_no_auth_user(self):
        pass