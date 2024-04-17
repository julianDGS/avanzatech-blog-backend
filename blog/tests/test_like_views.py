from rest_framework.status import *

from .setup import AuthenticateSetUp
from ..models import Like
from permission.tests.factories.permission_factories import PostWithPermissionFactory


class BlogPostWithAuthenticationTest(AuthenticateSetUp):


    def test_view_creates_like(self):
        self.assertFalse(self.user.is_admin)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 0)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.read)
        response = self.client.post('/like/', {'post_id': self.post_author.id}, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['post']['id'], self.post_author.id)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 1)

    
    def test_does_not_create_like_when_no_read_access(self):
        self.assertFalse(self.user.is_admin)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_team.id)), 0)
        PostWithPermissionFactory.create_batch(4, post=self.post_team, permission=self.none)
        response = self.client.post('/like/', {'post_id': self.post_team.id}, format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_team.id)), 0)
               

    def test_view_creates_unique_like_per_user(self):
        self.assertFalse(self.user.is_admin)
        Like.objects.create(post=self.post_author, user=self.user)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 1)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.read)
        response = self.client.post('/like/',{'post_id': self.post_author.id}, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], "The fields post, user must make a unique set.")
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 1)


    def test_view_deletes_like(self):
        self.assertFalse(self.user.is_admin)
        Like.objects.create(post=self.post_author, user=self.user)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 1)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.read)
        response = self.client.delete(f'/like/{self.post_author.id}/')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 0)


    def test_does_not_delete_like_when_no_read_access(self):
        self.assertFalse(self.user.is_admin)
        Like.objects.create(post=self.post_author, user=self.user)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 1)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.none)
        response = self.client.delete(f'/like/{self.post_author.id}/')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 1)


    def test_view_creates_like_from_admin_without_permissions(self):
        admin = self.user
        admin.is_admin = True
        admin.save()
        self.assertTrue(self.user.is_admin)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 0)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.none)
        response = self.client.post('/like/', {'post_id': self.post_author.id}, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['post']['id'], self.post_author.id)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 1)

    

