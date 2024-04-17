from django.urls import reverse
from rest_framework.status import *

from blog.tests.factories.blog_post_factories import CommentFactory, LikeFactory
from permission.models import PostPermission

from .setup import AuthenticateSetUp
from ..models import Comment
from permission.tests.factories.permission_factories import PostWithPermissionFactory


class BlogPostWithAuthenticationTest(AuthenticateSetUp):


    def test_view_creates_like(self):
        self.assertFalse(self.user.is_admin)
        self.assertEqual(len(Comment.objects.filter(post_id=self.post_author.id)), 0)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.read)
        response = self.client.post(
            self.comment_url, 
            {'post_id': self.post_author.id, 'comment': 'some comment for some post from some user'}, 
            format='json'
        )
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['post']['id'], self.post_author.id)
        self.assertEqual(len(Comment.objects.filter(post_id=self.post_author.id)), 1)

    
    def test_does_not_create_comment_when_no_read_access(self):
        self.assertFalse(self.user.is_admin)
        self.assertEqual(len(Comment.objects.filter(post_id=self.post_team.id)), 0)
        PostWithPermissionFactory.create_batch(4, post=self.post_team, permission=self.none)
        response = self.client.post(
            self.comment_url, 
            {'post_id': self.post_team.id, 'comment': 'some comment for some post from some user'}, 
            format='json'
        )
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(len(Comment.objects.filter(post_id=self.post_team.id)), 0)


    def test_view_creates_comment_from_admin_without_permissions(self):
            admin = self.user
            admin.is_admin = True
            admin.save()
            self.assertTrue(self.user.is_admin)
            self.assertEqual(len(Comment.objects.filter(post_id=self.post_author.id)), 0)
            PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.none)
            response = self.client.post(
                self.comment_url, 
                {'post_id': self.post_author.id, 'comment': 'some comment for some post from some user'}, 
                format='json'
            )
            self.assertEqual(response.status_code, HTTP_201_CREATED)
            self.assertEqual(response.data['post']['id'], self.post_author.id)
            self.assertEqual(len(Comment.objects.filter(post_id=self.post_author.id)), 1)


  
        

    

