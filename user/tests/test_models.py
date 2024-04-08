from django.test import TestCase
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError

from ..models import User, Team
from .factories.user_factories import * 
# Create your tests here.

class UserModelTest(TestCase):
    
    def test_user_exist(self):
        user = User.objects.all()

        self.assertEqual(user.count(), 0)

    def test_create_new_user(self):

        user = UserFactory(email='probe@mail.com')
        nickname = 'probe'

        users_from_db = User.objects.all()
        self.assertEqual(len(users_from_db), 1)
        
        user_created = users_from_db[0]
        self.assertEqual(user.email, user_created.email)
        self.assertEqual(user.team.id, user_created.team.id)
        self.assertEqual(nickname, user_created.nickname)
        self.assertTrue(check_password('1234', user_created.password))


    def test_validate_unique_fields(self):
        UserFactory(email='probe@mail.com')
        
        with self.assertRaises(IntegrityError):
            user2 = User()
            user2.email = 'probe@mail.com'
            user2.set_password('1234')
            user2.save()

    def test_required_team_fields(self):
        with self.assertRaises(IntegrityError):
            team = Team()
            team.save()

    def test_delete_team(self):
        team = TeamFactory()
        UserFactory(team=team)
        
        user_from_db = User.objects.first()
        self.assertEqual(user_from_db.team.id, team.id)

        team.delete()
        user_from_db = User.objects.first()
        self.assertEqual(user_from_db.team, None)
