from rest_framework.test import APITestCase
from rest_framework.status import *

from blog.tests.factories.blog_post_factories import BlogPostFactory
from permission.models import Category, CategoryName, Permission, PermissionName, PostPermission
from permission.tests.factories.permission_factories import PostWithPermissionFactory
from user.tests.factories.user_factories import TeamFactory, UserFactory
from ..models import BlogPost, Like, Comment
from user.models import User

class BlogPostWithNoAuthTest(APITestCase):

    def setUp(self):
        self.post_url = '/post/'
        self.user = User.objects.create_user(email="admin2@mail.com", password="223344")
        public = Category.objects.create(name=CategoryName.PUBLIC)
        auth = Category.objects.create(name=CategoryName.AUTHENTICATE)
        team = Category.objects.create(name=CategoryName.TEAM)
        author = Category.objects.create(name=CategoryName.AUTHOR)
        self.read = Permission.objects.create(name=PermissionName.READ)
        self.edit = Permission.objects.create(name=PermissionName.EDIT)
        self.none = Permission.objects.create(name=PermissionName.NONE)
        self.data = {
            'title': 'Leave sense plan.', 
            'content': 'Effect somebody drug figure quality success. There government work commercial.',
            'author': self.user.id,
            'permissions': [
                {"category_id": public.id, "permission_id": self.none.id},
                {"category_id": auth.id, "permission_id": self.read.id},
                {"category_id": team.id, "permission_id": self.edit.id},
                {"category_id": author.id, "permission_id": self.edit.id}
            ]
        }

    def test_view_does_not_create_post_with_no_auth_user(self): 
        response = self.client.post(self.post_url, self.data, format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertFalse(BlogPost.objects.all())
        self.assertFalse(PostPermission.objects.all())

    def test_view_does_not_update_post_with_no_auth_user(self):
        post = BlogPostFactory(author=self.user)
        PostWithPermissionFactory.create_batch(4, post=post)
        response = self.client.put(f'{self.post_url}{post.id}/', self.data, format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_view_updates_post_with_public_edit(self):
        post = BlogPostFactory(author=self.user)
        PostWithPermissionFactory.create_batch(4, post=post, permission=self.edit)
        response = self.client.put(f'{self.post_url}{post.id}/', self.data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_view_shows_correct_posts_with_no_auth_user(self):
        self.assertFalse(self.user.is_admin)
        post_author = BlogPostFactory(author=self.user)
        post_team = BlogPostFactory(author=UserFactory(team=self.user.team))
        post_authenticate = BlogPostFactory(author=UserFactory(team=TeamFactory(name='other team')))
        PostWithPermissionFactory.create_batch(4, post=post_author, permission=self.none)
        PostWithPermissionFactory.create_batch(4, post=post_team, permission=self.none)
        PostWithPermissionFactory.create_batch(4, post=post_authenticate, permission=self.edit)
        permissions = PostPermission.objects.all()
        self.assertTrue(len(permissions), 4)

        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_view_shows_404_when_retrieve_and_no_auth_user(self):
        self.assertFalse(self.user.is_admin)
        post_author = BlogPostFactory(author=self.user)
        PostWithPermissionFactory.create_batch(4, post=post_author, permission=self.read)
        response = self.client.get(f'{self.post_url}{post_author.id}/')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_view_can_handle_likes_from_anonymous_user(self):
        self.assertFalse(self.user.is_admin)
        post_author = BlogPostFactory(author=self.user)
        self.assertEqual(len(Like.objects.filter(post_id=post_author.id)), 0)
        PostWithPermissionFactory.create_batch(4, post=post_author, permission=self.read)
        response = self.client.post('/like/', {'post_id': post_author.id}, format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(len(Like.objects.filter(post_id=post_author.id)), 0)
    
    def test_view_can_handle_comments_from_anonymous_user(self):
        self.assertFalse(self.user.is_admin)
        post_author = BlogPostFactory(author=self.user)
        self.assertEqual(len(Comment.objects.filter(post_id=post_author.id)), 0)
        PostWithPermissionFactory.create_batch(4, post=post_author, permission=self.read)
        response = self.client.post('/comment/', {'post_id': post_author.id, 'comment': 'some comment'}, format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(len(Comment.objects.filter(post_id=post_author.id)), 0)