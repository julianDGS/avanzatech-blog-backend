from datetime import datetime
from django.test import TestCase
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError

from ..models import BlogPost
from .factories.blog_post_factories import *
# Create your tests here.

class UserModelTest(TestCase):

    def test_blog_post_exist(self):
        blog_post = BlogPost.objects.all()

        self.assertEqual(blog_post.count(), 0)

    def test_create_new_blog_post(self):        
        blog_post = BlogPostFactory()
        created_date = datetime.now().date()
        excerpt = blog_post.content[:200]
        
        posts_from_db = BlogPost.objects.all()
        self.assertEqual(len(posts_from_db), 1)
        
        post_created = posts_from_db[0]
        self.assertEqual(blog_post.title, post_created.title)
        self.assertEqual(blog_post.user.id, post_created.user.id)
        self.assertEqual(post_created.excerpt, excerpt)
        self.assertEqual(post_created.created_at, post_created.updated_at.date())
        self.assertEqual(post_created.created_at, created_date)

    def test_validate_required_fields(self):
        with self.assertRaises(IntegrityError):
            blog_post = BlogPost()
            blog_post.save()