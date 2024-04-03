import factory

from blog.models import BlogPost
from user.models import User, Team

class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team
    
    name = factory.Faker('job')

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    email = 'probe@mail.com'
    team = factory.SubFactory(TeamFactory)

    @factory.post_generation
    def set_user_password(obj, create, extracted, **kwargs):
        if not create:
            # When a related instance (sub factory) is being created and userFactory is already created
            return
        if extracted:
            # If I set a value for password creating an instance of this factory
            obj.set_password(extracted)
        else:
            obj.set_password('1234')

class BlogPostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlogPost

    title = factory.Faker('sentence', nb_words=4)
    content = factory.Faker('paragraph', nb_sentences=10)
    user = factory.SubFactory(UserFactory)

    # def build_blog_post_JSON(cls):
    #     return factory.build(dict, FACTORY_CLASS=BlogPostFactory)
        # return {
        #     'ruc': str(self.faker.random_number(digits=11)),
        #     'business_name': self.faker.company(),
        #     'address': self.faker.address(),
        #     'phone': str(self.faker.random_number(digits=11)),
        #     'email': self.faker.email()
        # }