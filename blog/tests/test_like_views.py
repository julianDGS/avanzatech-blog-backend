from django.urls import reverse
from rest_framework.status import *

from blog.tests.factories.blog_post_factories import LikeFactory
from permission.models import PostPermission

from .setup import AuthenticateSetUp
from ..models import Like
from permission.tests.factories.permission_factories import PostWithPermissionFactory


class BlogPostWithAuthenticationTest(AuthenticateSetUp):


    def test_view_creates_like(self):
        self.assertFalse(self.user.is_admin)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 0)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.read)
        response = self.client.post(self.like_url, {'post_id': self.post_author.id}, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['post']['id'], self.post_author.id)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 1)

    
    def test_does_not_create_like_when_no_read_access(self):
        self.assertFalse(self.user.is_admin)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_team.id)), 0)
        PostWithPermissionFactory.create_batch(4, post=self.post_team, permission=self.none)
        response = self.client.post(self.like_url, {'post_id': self.post_team.id}, format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_team.id)), 0)
               

    def test_view_creates_unique_like_per_user(self):
        self.assertFalse(self.user.is_admin)
        LikeFactory.create(post=self.post_author, user=self.user)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 1)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.read)
        response = self.client.post(self.like_url,{'post_id': self.post_author.id}, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], "The fields post, user must make a unique set.")
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 1)


    def test_view_deletes_like(self):
        self.assertFalse(self.user.is_admin)
        LikeFactory.create(post=self.post_author, user=self.user)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 1)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.read)
        response = self.client.delete(f'{self.like_url}{self.post_author.id}/')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 0)


    def test_does_not_delete_like_when_no_read_access(self):
        self.assertFalse(self.user.is_admin)
        LikeFactory.create(post=self.post_author, user=self.user)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 1)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.none)
        response = self.client.delete(f'{self.like_url}{self.post_author.id}/')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 1)


    def test_view_creates_like_from_admin_without_permissions(self):
        admin = self.user
        admin.is_admin = True
        admin.save()
        self.assertTrue(self.user.is_admin)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 0)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.none)
        response = self.client.post(self.like_url, {'post_id': self.post_author.id}, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['post']['id'], self.post_author.id)
        self.assertEqual(len(Like.objects.filter(post_id=self.post_author.id)), 1)

    
    def test_view_shows_correct_likes_with_user_as_author(self):
        self.assertFalse(self.user.is_admin)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.read)
        PostWithPermissionFactory.create_batch(4, post=self.post_team, permission=self.read)
        PostWithPermissionFactory.create_batch(4, post=self.post_authenticate, permission=self.read)
        LikeFactory.create_batch(4, post=self.post_author)
        LikeFactory.create_batch(4, post=self.post_team)
        LikeFactory.create_batch(4, post=self.post_authenticate)

        test_data = [
            {'category': self.author, 'post': self.post_author, 'len': 8},
            {'category': self.team, 'post': self.post_team, 'len': 4},
            {'category': self.auth, 'post': self.post_authenticate, 'len': 0},
        ]

        for data in test_data:
            with self.subTest(data=data):
                post_data = data['post']
                PostPermission.objects.filter(post=post_data, category=data['category']).update(permission=self.none)
                response = self.client.get(self.like_url)
                self.assertEqual(response.status_code, HTTP_200_OK)
                self.assertEqual(len(response.data['results']), data['len'])


    def test_view_shows_correct_likes_with_user_as_team_member(self):
        response_login = self.client.post(reverse('login'),{'username': self.post_team.author.email, 'password': '1234'}, format='json')
        self.assertFalse(self.post_team.author.is_admin)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.edit)
        PostWithPermissionFactory.create_batch(4, post=self.post_team, permission=self.read)
        PostWithPermissionFactory.create_batch(4, post=self.post_authenticate, permission=self.read)
        LikeFactory.create_batch(4, post=self.post_author)
        LikeFactory.create_batch(4, post=self.post_team)
        LikeFactory.create_batch(4, post=self.post_authenticate)

        test_data = [
            {'category': self.author, 'post': self.post_author, 'len': 12},
            {'category': self.team, 'post': self.post_team, 'len': 12},
            {'category': self.auth, 'post': self.post_authenticate, 'len': 8},
        ]

        for data in test_data:
            with self.subTest(data=data):
                post_data = data['post']
                PostPermission.objects.filter(post=post_data, category=data['category']).update(permission=self.none)
                response = self.client.get(self.like_url, headers={'X-CSRFToken': response_login.cookies['csrftoken'].value})
                self.assertEqual(response.status_code, HTTP_200_OK)
                self.assertEqual(len(response.data['results']), data['len'])


    def test_view_shows_correct_likes_with_user_as_authenticated(self):
        response_login = self.client.post(reverse('login'),{'username': self.post_authenticate.author.email, 'password': '1234'}, format='json')
        self.assertFalse(self.post_authenticate.author.is_admin)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.read)
        PostWithPermissionFactory.create_batch(4, post=self.post_team, permission=self.read)
        PostWithPermissionFactory.create_batch(4, post=self.post_authenticate, permission=self.edit)
        LikeFactory.create_batch(4, post=self.post_author)
        LikeFactory.create_batch(4, post=self.post_team)
        LikeFactory.create_batch(4, post=self.post_authenticate)

        test_data = [
            {'category': self.author, 'post': self.post_author, 'len': 12},
            {'category': self.team, 'post': self.post_team, 'len': 12},
            {'category': self.auth, 'post': self.post_authenticate, 'len': 12},
        ]

        for data in test_data:
            with self.subTest(data=data):
                post_data = data['post']
                PostPermission.objects.filter(post=post_data, category=data['category']).update(permission=self.none)
                response = self.client.get(self.like_url, headers={'X-CSRFToken': response_login.cookies['csrftoken'].value})
                self.assertEqual(response.status_code, HTTP_200_OK)
                self.assertEqual(len(response.data['results']), data['len'])


    def test_view_filter_by_post_and_user(self):
        self.assertFalse(self.post_author.author.is_admin)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.read)
        LikeFactory.create(post=self.post_author, user=self.user)
        LikeFactory.create_batch(3, post=self.post_author)

        test_data = [
            {'param' : f'post={self.post_author.id}', 'len': 4},
            {'param' : f'user={self.user.id}', 'len': 1},
            {'param' : f'post={self.post_author.id}&user={self.user.id}', 'len': 1}
        ]

        for data in test_data:
            with self.subTest(data=data):
                param = data['param']
                response = self.client.get(f'{self.like_url}?{param}')
                self.assertEqual(response.status_code, HTTP_200_OK)
                self.assertEqual(len(response.data['results']), data['len'])


    def test_view_pagination_includes_necessary_arguments(self):
        # current page, total pages, total count, next page URL, previous page URL. 20 items per page
        admin = self.user
        admin.is_admin = True
        admin.save()
        LikeFactory.create_batch(40)
        response = self.client.get(self.like_url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['total_pages'], 2)
        self.assertEqual(response.data['total_count'], 40)
        self.assertEqual(response.data['current_page'], 1)
        next_page_param = (response.data['next']).find('?')
        self.assertEqual(response.data['next'][next_page_param:], '?page=2')
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(len(response.data['results']), 20)
        

    

