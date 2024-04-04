import factory

from user.models import User, Team

class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team
    
    name = factory.Faker('word')

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    email = factory.Faker('email')
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