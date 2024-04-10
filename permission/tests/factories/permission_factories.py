import factory

from ...models import CategoryName, Permission, Category, PermissionName, PostPermission
from blog.tests.factories.blog_post_factories import BlogPostFactory

class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission
        django_get_or_create = ("name",)

    name = factory.Iterator([choice for choice, _ in PermissionName.choices])

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)
    name = factory.Iterator([choice for choice, _ in CategoryName.choices])

class PostWithPermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostPermission

    post = factory.SubFactory(BlogPostFactory)
    permission = factory.SubFactory(PermissionFactory)
    category = factory.SubFactory(CategoryFactory)
