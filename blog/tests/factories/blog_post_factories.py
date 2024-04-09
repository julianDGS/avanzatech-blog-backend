import factory

from blog.models import BlogPost, Comment
from user.tests.factories.user_factories import UserFactory

class BlogPostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlogPost

    title = factory.Faker('sentence', nb_words=4)
    content = factory.Faker('paragraph', nb_sentences=10)
    author = factory.SubFactory(UserFactory)

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(BlogPostFactory)
    comment = factory.Faker('paragraph', nb_sentences=7)

class PostWith2CommentsFactory(BlogPostFactory): 
    c = factory.RelatedFactoryList(
        CommentFactory,
        factory_related_name='post',
        size=2
    )

class UserWith2CommentsFactory(UserFactory):
    c = factory.RelatedFactoryList(
        CommentFactory,
        factory_related_name='user',
        size=2
    )