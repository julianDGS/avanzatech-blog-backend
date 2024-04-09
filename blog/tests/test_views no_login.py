from django.test import TestCase
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.status import *

from ..models import User
from .factories.blog_post_factories import * 

class BlogPostWithNoAuthTest(TestCase):

    def test_view_does_not_create_post_with_no_auth_user(self):
        pass

    def test_view_shows_correct_posts_with_no_auth_user(self):
        pass