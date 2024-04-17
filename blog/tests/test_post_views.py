from django.urls import reverse
from rest_framework.response import Response
from rest_framework.status import *

from .setup import AuthenticateSetUp
from ..models import BlogPost
from permission.models import PostPermission
from .factories.blog_post_factories import BlogPostFactory
from permission.tests.factories.permission_factories import PostWithPermissionFactory


class BlogPostWithAuthenticationTest(AuthenticateSetUp):


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
        self.assertEqual(response.data['permissions'][0], "Category matching query does not exist.")


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
        self.assertEqual(response.data['permissions'][0], "Permission matching query does not exist.")
    

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


    def test_view_updates_post_data_including_permissions(self):
        post = BlogPostFactory(author=self.user)
        PostWithPermissionFactory(post=post, category=self.public, permission=self.read)
        PostWithPermissionFactory(post=post, category=self.auth, permission=self.none)
        PostWithPermissionFactory(post=post, category=self.team, permission=self.edit)
        PostWithPermissionFactory(post=post, category=self.author, permission=self.edit)
        permissions = PostPermission.objects.all()
        self.assertEqual(permissions[0].category.name, 'public')
        self.assertEqual(permissions[1].category.name, 'auth')
        self.assertEqual(permissions[2].category.name, 'team')
        self.assertEqual(permissions[3].category.name, 'author')

        response: Response = self.client.put(f'{self.post_url}{post.id}/', self.data, format='json')
        permissions = PostPermission.objects.all()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(len(permissions), 4)
        self.assertEqual(response.data['id'], post.id)
        self.assertDictEqual(
            {permission.category.id: permission.permission.id for permission in permissions}, 
            {permission['category_id']: permission['permission_id'] for permission in self.data['permissions']}
        )
        self.assertEqual(response.data['title'], self.data['title'])
        self.assertEqual(response.data['content'], self.data['content'])


    def test_view_can_handle_wrong_data_on_update(self):
        post = BlogPostFactory(author=self.user)
        PostWithPermissionFactory(post=post, category=self.public, permission=self.edit)
        PostWithPermissionFactory(post=post, category=self.auth, permission=self.edit)
        PostWithPermissionFactory(post=post, category=self.team, permission=self.edit)
        PostWithPermissionFactory(post=post, category=self.author, permission=self.edit)
        permissions = PostPermission.objects.all()
        self.assertTrue(len(permissions), 4)
        
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
            {**self.data, 'permissions': [
                {'category_id': self.public.id, 'permission_id': self.read.id}, 
                {'category_id': self.public.id, 'permission_id': self.read.id},
                {'category_id': self.team.id, 'permission_id': self.read.id},
                {'category_id': self.team.id, 'permission_id': self.read.id}
            ]},
            {**self.data, 'permissions': [
                {'category_id': self.public.id, 'permission_id': self.read.id}, 
                {'category_id': self.auth.id, 'permission_id': self.read.id},
                {'category_id': self.team.id, 'permission_id': self.read.id},
                {'category_id': self.author.id, 'permission_id': -1}
            ]}
        ]

        for data in test_data:    
            with self.subTest(data=data):
                response: Response = self.client.post(self.post_url, data, format='json')
                self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)


    def test_view_updates_only_necesary_fields(self):
        post = BlogPostFactory(author=self.user)
        PostWithPermissionFactory(post=post, category=self.public, permission=self.edit)
        PostWithPermissionFactory(post=post, category=self.auth, permission=self.edit)
        PostWithPermissionFactory(post=post, category=self.team, permission=self.edit)
        PostWithPermissionFactory(post=post, category=self.author, permission=self.edit)
        permissions = PostPermission.objects.all()
        self.assertTrue(len(permissions), 4)
        
        data = {**self.data, 'author': -1, 'id': -1}
        
        response: Response = self.client.put(f'{self.post_url}{post.id}/', data, format='json')
        permissions = PostPermission.objects.all()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(len(permissions), 4)
        self.assertEqual(response.data['id'], post.id)
        self.assertEqual(response.data['author'], self.user.id)


    def test_view_does_not_update_post_with_no_edit_permissions_by_user(self):
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.edit)
        PostWithPermissionFactory.create_batch(4, post=self.post_team, permission=self.edit)
        PostWithPermissionFactory.create_batch(4, post=self.post_authenticate, permission=self.edit)
        permissions = PostPermission.objects.all()
        self.assertTrue(len(permissions), 4)

        test_data = [
            {'categories': (self.author,), 'post': self.post_author},
            {'categories': (self.team,), 'post': self.post_team},
            {'categories': (self.auth,), 'post': self.post_authenticate},
            {'categories': (self.author, self.team), 'post': self.post_author},
            {'categories': (self.auth, self.team), 'post': self.post_team},
            {'categories': (self.author, self.auth), 'post': self.post_authenticate},
            {'categories': (self.author, self.team), 'post': self.post_team},
            {'categories': (self.auth, self.team), 'post': self.post_authenticate},
            {'categories': (self.author, self.auth), 'post': self.post_author},
        ]

        for data in test_data:
            with self.subTest(data=data):
                post_data = data['post']
                PostPermission.objects.filter(post=post_data, category__in=data['categories']).update(permission=self.none)
                response: Response = self.client.put(f'{self.post_url}{post_data.id}/', self.data, format='json')
                self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
                PostPermission.objects.filter(post=post_data, category__in=data['categories']).update(permission=self.edit)


    def test_view_update_post_with_no_edit_permissions_by_admin_user(self):
        admin = self.user
        admin.is_admin = True
        admin.save()
        post = BlogPostFactory(author=admin)
        PostWithPermissionFactory.create_batch(4, post=post, permission=self.none)
        self.assertTrue(len(PostPermission.objects.all()), 4)
        
        response: Response = self.client.put(f'{self.post_url}{post.id}/', self.data, format='json')
        permissions = PostPermission.objects.all()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['id'], post.id)
        self.assertDictEqual(
            {permission.category.id: permission.permission.id for permission in permissions}, 
            {permission['category_id']: permission['permission_id'] for permission in self.data['permissions']}
        )
        self.assertEqual(response.data['title'], self.data['title'])
        self.assertEqual(response.data['content'], self.data['content'])
    
    def test_view_deletes_post(self):
        self.assertEqual(len(BlogPost.objects.filter(pk=self.post_author.id)), 1)
        response = self.client.delete(f'{self.post_url}{self.post_author.id}/')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(len(BlogPost.objects.filter(pk=self.post_author.id)), 0)


    def test_view_deletes_post_only_by_author(self):
        self.assertEqual(len(BlogPost.objects.filter(pk=self.post_team.id)), 1)
        response = self.client.delete(f'{self.post_url}{self.post_team.id}/')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(len(BlogPost.objects.filter(pk=self.post_team.id)), 1)


    def test_view_admin_can_delete_post_without_permissions(self):
        admin = self.user
        admin.is_admin = True
        admin.save()
        self.assertEqual(len(BlogPost.objects.filter(pk=self.post_team.id)), 1)
        response = self.client.delete(f'{self.post_url}{self.post_team.id}/')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(len(BlogPost.objects.filter(pk=self.post_team.id)), 0)


    def test_view_shows_correct_posts_with_user_as_author(self):
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.read)
        PostWithPermissionFactory.create_batch(4, post=self.post_team, permission=self.read)
        PostWithPermissionFactory.create_batch(4, post=self.post_authenticate, permission=self.read)
        permissions = PostPermission.objects.all()
        self.assertTrue(len(permissions), 4)

        test_data = [
            {'category': self.author, 'post': self.post_author, 'len': 2},
            {'category': self.team, 'post': self.post_team, 'len': 1},
            {'category': self.auth, 'post': self.post_authenticate, 'len': 0},
        ]

        for data in test_data:
            with self.subTest(data=data):
                post_data = data['post']
                PostPermission.objects.filter(post=post_data, category=data['category']).update(permission=self.none)
                response = self.client.get(self.post_url)
                self.assertEqual(response.status_code, HTTP_200_OK)
                self.assertEqual(len(response.data['results']), data['len'])


    def test_view_shows_correct_posts_with_user_as_team_member(self):
        response_login = self.client.post(reverse('login'),{'username': self.post_team.author.email, 'password': '1234'}, format='json')
        self.assertFalse(self.post_team.author.is_admin)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.edit)
        PostWithPermissionFactory.create_batch(4, post=self.post_team, permission=self.read)
        PostWithPermissionFactory.create_batch(4, post=self.post_authenticate, permission=self.read)
        permissions = PostPermission.objects.all()
        self.assertTrue(len(permissions), 4)

        test_data = [
            {'categories': (self.author,), 'post': self.post_author, 'len': 3},
            {'categories': (self.team,), 'post': self.post_team, 'len': 3},
            {'categories': (self.auth,), 'post': self.post_authenticate, 'len': 2},
        ]

        for data in test_data:
            with self.subTest(data=data):
                post_data = data['post']
                PostPermission.objects.filter(post=post_data, category__in=data['categories']).update(permission=self.none)
                response = self.client.get(self.post_url, headers={'X-CSRFToken': response_login.cookies['csrftoken'].value})
                self.assertEqual(response.status_code, HTTP_200_OK)
                self.assertEqual(len(response.data['results']), data['len'])


    def test_view_shows_correct_posts_with_user_as_authenticated(self):
        response_login = self.client.post(reverse('login'),{'username': self.post_authenticate.author.email, 'password': '1234'}, format='json')
        self.assertFalse(self.post_authenticate.author.is_admin)
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.read)
        PostWithPermissionFactory.create_batch(4, post=self.post_team, permission=self.read)
        PostWithPermissionFactory.create_batch(4, post=self.post_authenticate, permission=self.edit)
        permissions = PostPermission.objects.all()
        self.assertTrue(len(permissions), 4)

        test_data = [
            {'categories': (self.author,), 'post': self.post_author, 'len': 3},
            {'categories': (self.team,), 'post': self.post_team, 'len': 3},
            {'categories': (self.auth,), 'post': self.post_authenticate, 'len': 3},
        ]

        for data in test_data:
            with self.subTest(data=data):
                post_data = data['post']
                PostPermission.objects.filter(post=post_data, category__in=data['categories']).update(permission=self.none)
                response = self.client.get(self.post_url, headers={'X-CSRFToken': response_login.cookies['csrftoken'].value})
                self.assertEqual(response.status_code, HTTP_200_OK)
                self.assertEqual(len(response.data['results']), data['len'])


    def test_view_shows_empty_list_if_no_post_retrieved(self):
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.none)
        PostWithPermissionFactory.create_batch(4, post=self.post_team, permission=self.none)
        PostWithPermissionFactory.create_batch(4, post=self.post_authenticate, permission=self.none)
        permissions = PostPermission.objects.all()
        self.assertTrue(len(permissions), 4)
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)


    def test_view_shows_404_if_no_valid_access_to_post(self):
        PostWithPermissionFactory.create_batch(4, post=self.post_author, permission=self.read)
        PostWithPermissionFactory.create_batch(4, post=self.post_team, permission=self.none)
        PostWithPermissionFactory.create_batch(4, post=self.post_authenticate, permission=self.edit)
        test_data = [
            {'post': self.post_author, 'status': HTTP_200_OK},
            {'post': self.post_team, 'status': HTTP_403_FORBIDDEN},
            {'post': self.post_authenticate, 'status': HTTP_200_OK},
        ]
        for data in test_data:
            with self.subTest(data=data):
                post = data['post']
                status = data['status']
                response = self.client.get(f'{self.post_url}{post.id}/')
                self.assertEqual(response.status_code, status)


    def test_view_pagination_includes_necessary_arguments(self):
        # current page, total pages, total count, next page URL, previous page URL. 10 items per page
        admin = self.user
        admin.is_admin = True
        admin.save()
        BlogPostFactory.create_batch(47)
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['total_pages'], 5)
        self.assertEqual(response.data['total_count'], 50)
        self.assertEqual(response.data['current_page'], 1)
        next_page_param = (response.data['next']).find('?')
        self.assertEqual(response.data['next'][next_page_param:], '?page=2')
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(len(response.data['results']), 10)

    
