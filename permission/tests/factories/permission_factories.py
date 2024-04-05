import factory

from ...models import Permission, Category, PostPermission
from blog.tests.factories.blog_post_factories import BlogPostFactory

class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission
    # name = factory.Iterator([choice for choice, name in PermissionName.choices])

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    # name = factory.Iterator([choice for choice, name in CategoryName.choices])

class PostWithPermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostPermission

    post = factory.SubFactory(BlogPostFactory)
