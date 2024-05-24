from permission.tests.factories.permission_factories import PermissionFactory, CategoryFactory
from permission.models import PermissionName, CategoryName
from user.models import User, Team


def create_categories():
    CategoryFactory(name=CategoryName.PUBLIC)
    CategoryFactory(name=CategoryName.AUTHENTICATE)
    CategoryFactory(name=CategoryName.TEAM)
    CategoryFactory(name=CategoryName.AUTHOR)

def create_permissions():
    PermissionFactory(name=PermissionName.READ)
    PermissionFactory(name=PermissionName.EDIT)
    PermissionFactory(name=PermissionName.NONE)

def create_team():
    team = Team.objects.first();
    if not team:
        Team.objects.create(id=1, name='rookie')
    elif team.id != 1:
        team.delete()
        Team.objects.create(id=1, name='rookie')

def init_data():
    create_team()
    create_categories()
    create_permissions()
    print("Initial data for categories and permissions loaded")
    user = User.objects.filter(pk=1).first()
    if not user:
        user = User.objects.create_superuser(id=1, email="superadmin@mail.com", password="admin")
    print("Superuser loaded with email: ", user.email)

init_data()
