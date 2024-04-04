from datetime import datetime
from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from ..models import Permission, PermissionName, Category, CategoryName
from .factories.permission_factories import *

class PermissionTest(TestCase):

    def test_permission_exist(self):
        permission = Permission.objects.all()

        self.assertEqual(permission.count(), 0)

    def test_create_new_read_permission(self):        
        permission = Permission(name=PermissionName.READ)
        permission.save()
        created_date = datetime.now().date()
        
        permissions_from_db = Permission.objects.all()
        self.assertEqual(len(permissions_from_db), 1)
        
        permission_created = permissions_from_db[0]
        self.assertEqual('read', permission_created.name)
        self.assertTrue(permission.id)
        self.assertEqual(permission_created.created_at, permission_created.updated_at.date())
        self.assertEqual(permission_created.created_at, created_date)
    
    def test_create_new_edit_permission(self):        
        permission = Permission(name=PermissionName.EDIT)
        permission.save()
        created_date = datetime.now().date()
        
        permissions_from_db = Permission.objects.all()
        self.assertEqual(len(permissions_from_db), 1)
        
        permission_created = permissions_from_db[0]
        self.assertEqual('edit', permission_created.name)
        self.assertTrue(permission.id)
        self.assertEqual(permission_created.created_at, permission_created.updated_at.date())
        self.assertEqual(permission_created.created_at, created_date)

    def test_validate_required_fields(self):
        with self.assertRaises(IntegrityError):
            permission = Permission()
            permission.save()

class CategoryTest(TestCase):

    def test_category_exist(self):
        category = Category.objects.all()

        self.assertEqual(category.count(), 0)

    def test_create_new_public_category(self):        
        category = Category(name=CategoryName.PUBLIC)
        created_date = datetime.now().date()
        category.save()
        
        categories_from_db = Category.objects.all()
        self.assertEqual(len(categories_from_db), 1)
        
        category_created = categories_from_db[0]
        self.assertEqual(category.name, 'public')
        self.assertTrue(category.id)
        self.assertEqual(category_created.created_at, category_created.updated_at.date())
        self.assertEqual(category_created.created_at, created_date)

    def test_validate_required_fields(self):
        with self.assertRaises(IntegrityError):
            category = Category()
            category.save()

class PostPermissionTest(TestCase):

    def test_post_permission_exist(self):
        category = PostPermission.objects.all()

        self.assertEqual(category.count(), 0)

    def test_create_post_with_permission(self):
        post = BlogPostFactory()
        post_permission = PostWithPermissionFactory(post=post)

        posts_from_db = PostPermission.objects.all()
        self.assertEqual(len(posts_from_db), 1)
        
        post_created = posts_from_db[0].post
        self.assertEqual(post.id , post_created.id)

    