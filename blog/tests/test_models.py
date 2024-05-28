from datetime import datetime
from django.test import TestCase
from django.db import IntegrityError

from ..models import BlogPost, Like, Comment
from .factories.blog_post_factories import *

class BlogModelTest(TestCase):

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
        self.assertEqual(blog_post.author.id, post_created.author.id)
        self.assertEqual(post_created.excerpt, excerpt)
        self.assertEqual(post_created.created_at.date(), post_created.updated_at.date())
        self.assertEqual(post_created.created_at.date(), created_date)

    def test_validate_required_fields(self):
        with self.assertRaises(IntegrityError):
            blog_post = BlogPost()
            blog_post.save()

class LikeModelTest(TestCase):

    def test_like_exist(self):
        like = Like.objects.all()

        self.assertEqual(like.count(), 0)

    def test_create_new_like(self):        
        user = UserFactory()
        post = BlogPostFactory()
        
        like = Like.objects.create(user=user, post=post)
        
        likes_from_db = Like.objects.all()
        self.assertEqual(len(likes_from_db), 1)
        
        like_created = likes_from_db[0]
        self.assertEqual(like.post.id, like_created.post.id)
        self.assertEqual(like.user.id, like_created.user.id)

    def test_validate_unique_like_per_user_and_post(self):
        user = UserFactory()
        post = BlogPostFactory()

        like = Like(user=user, post=post)
        like.save()
        with self.assertRaises(IntegrityError):
            like2 = Like(user=user, post=post)
            like2.save()

    def test_delete_likes_when_user_deleted(self):
        user = UserFactory()
        user2 = UserFactory()
        post = BlogPostFactory()
        post2 = BlogPostFactory()

        Like.objects.create(user=user, post=post)
        Like.objects.create(user=user, post=post2)
        Like.objects.create(user=user2, post=post2)
        likes_from_db = Like.objects.filter(user_id=user.id)
        self.assertEqual(len(likes_from_db), 2)

        user.delete()
        likes_from_db = Like.objects.filter(user_id=user.id)
        likes_other_user = Like.objects.filter(user_id=user2.id)
        self.assertEqual(len(likes_from_db), 0)
        self.assertEqual(len(likes_other_user), 1)

    def test_delete_likes_when_post_deleted(self):
        user = UserFactory()
        user2 = UserFactory()
        post = BlogPostFactory()
        post2 = BlogPostFactory()

        Like.objects.create(user=user, post=post)
        Like.objects.create(user=user2, post=post)
        Like.objects.create(user=user2, post=post2)
        likes_from_db = Like.objects.filter(post_id=post.id)
        self.assertEqual(len(likes_from_db), 2)

        post.delete()
        likes_from_db = Like.objects.filter(post_id=post.id)
        likes_other_post = Like.objects.filter(post_id=post2.id)
        self.assertEqual(len(likes_from_db), 0)
        self.assertEqual(len(likes_other_post), 1)

class CommentModelTest(TestCase):

    def test_comment_exist(self):
        comment = Comment.objects.all()

        self.assertEqual(comment.count(), 0)

    def test_create_new_comment(self):        
        # user = UserFactory()
        post = BlogPostFactory()
        created_date = datetime.now().date()

        comment = CommentFactory(post=post)

        comments_from_db = Comment.objects.all()
        self.assertEqual(len(comments_from_db), 1)
        
        comment_created = comments_from_db[0]
        self.assertEqual(comment.post.id, comment_created.post.id)
        self.assertEqual(comment.user.id, comment_created.user.id)
        self.assertEqual(comment_created.created_at.date(), comment_created.updated_at.date())
        self.assertEqual(comment_created.created_at.date(), created_date)

    def test_delete_comments_when_user_deleted(self):
        user = UserWith2CommentsFactory()
        user2 = UserWith2CommentsFactory()

        comments_from_db = Comment.objects.filter(user_id=user.id)
        self.assertEqual(len(comments_from_db), 2)

        user.delete()
        comments_from_db = Comment.objects.filter(user_id=user.id)
        comments_other_user = Comment.objects.filter(user_id=user2.id)
        self.assertEqual(len(comments_from_db), 0)
        self.assertEqual(len(comments_other_user), 2)

    def test_delete_comments_when_post_deleted(self):
        post = PostWith2CommentsFactory()
        post2 = PostWith2CommentsFactory()
        comments_from_db = Comment.objects.filter(post_id=post.id)
        self.assertEqual(len(comments_from_db), 2)

        post.delete()
        comments_from_db = Comment.objects.filter(post_id=post.id)
        comments_other_post = Comment.objects.filter(post_id=post2.id)
        self.assertEqual(len(comments_from_db), 0)
        self.assertEqual(len(comments_other_post), 2)
    