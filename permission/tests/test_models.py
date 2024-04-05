from datetime import datetime
from django.test import TestCase
from django.db import IntegrityError

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

        public = CategoryFactory(name=CategoryName.PUBLIC)
        auth = CategoryFactory(name=CategoryName.AUTHENTICATE)
        team = CategoryFactory(name=CategoryName.TEAM)
        author = CategoryFactory(name=CategoryName.AUTHOR)
        
        read = PermissionFactory(name=PermissionName.READ)
        edit = PermissionFactory(name=PermissionName.EDIT)
        test_data = [
            {"category": public, "permission": read},
            {"category": auth, "permission": edit},
            {"category": team, "permission": None},
            {"category": author, "permission": edit},
        ]
        for data in test_data:
            with self.subTest(data=data):
                post_permission1 = PostWithPermissionFactory(post=post, category=data['category'], permission=data['permission'])
                posts_from_db = PostPermission.objects.filter(
                    post_id=post_permission1.post.id,
                    category_id=post_permission1.category.id
                )
                self.assertEqual(len(posts_from_db), 1)
                post_permission_db = posts_from_db.first()
                self.assertEqual(post_permission_db.category.id, post_permission1.category.id)
                self.assertEqual(post_permission_db.post.id, post_permission1.post.id)

    def test_unique_fields(self):
        post = BlogPostFactory()
        public = CategoryFactory(name=CategoryName.PUBLIC)
        read = PermissionFactory(name=PermissionName.READ)
        PostWithPermissionFactory(post=post, category=public, permission=None)

        with self.assertRaises(IntegrityError):
            PostWithPermissionFactory(post=post, category=public, permission=read)
    
    def test_delete_post_permission_when_delete_post(self):
        post = BlogPostFactory()
        post2 = BlogPostFactory()
        category1 = CategoryFactory(name="cat 1.1")
        category2 = CategoryFactory(name="cat 1.2")
        PostWithPermissionFactory(post=post, category=category1, permission=None)
        PostWithPermissionFactory(post=post2, category=category2, permission=None)
        
        posts_from_db = PostPermission.objects.all()
        self.assertEqual(len(posts_from_db), 2)
        
        post.delete()
        posts_from_db = PostPermission.objects.all()
        self.assertEqual(len(posts_from_db), 1)
        self.assertEqual(posts_from_db[0].post.id, post2.id)

    def test_delete_post_permission_when_delete_category(self):
        category = CategoryFactory(name="cat 2.1")
        category2 = CategoryFactory(name="cat 2.2")
        PostWithPermissionFactory(category=category, permission=None)
        PostWithPermissionFactory(category=category2, permission=None)
        
        posts_from_db = PostPermission.objects.all()
        self.assertEqual(len(posts_from_db), 2)
        
        category.delete()
        posts_from_db = PostPermission.objects.all()
        self.assertEqual(len(posts_from_db), 1)
        self.assertEqual(posts_from_db[0].category.id, category2.id)
    
    def test_delete_post_permission_when_delete_permission(self):
        permission = PermissionFactory(name="perm 3.1")
        permission2 = PermissionFactory(name="perm 3.2")
        category1 = CategoryFactory(name="cat 3.1")
        category2 = CategoryFactory(name="cat 3.2")
        PostWithPermissionFactory(permission=permission, category=category1)
        PostWithPermissionFactory(permission=permission2, category=category2)
        
        posts_from_db = PostPermission.objects.all()
        self.assertEqual(len(posts_from_db), 2)
        
        permission.delete()
        posts_from_db = PostPermission.objects.all()
        perm = posts_from_db.first().permission.id
        self.assertEqual(len(posts_from_db), 1)
        self.assertEqual(perm, permission2.id)      
                

    