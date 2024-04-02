from django.test import TestCase
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError

from ..models import User
# Create your tests here.

class UserModelTest(TestCase):
    
    def test_user_exist(self):
        user = User.objects.all()

        self.assertEqual(user.count(), 0)

    def test_create_new_user(self):
        user = User()
        user.email = 'probe@mail.com'
        user.set_password('1234')
        user.save()

        users_from_db = User.objects.all()
        self.assertEqual(len(users_from_db), 1)
        
        user_created = users_from_db[0]
        self.assertEqual(user.email, user_created.email)
        self.assertTrue(check_password('1234', user_created.password))


    def test_validate_unique_fields(self):
        user = User()
        user.email = 'probe@mail.com'
        user.set_password('1234')
        user.save()

        with self.assertRaises(IntegrityError):
            user2 = User()
            user2.email = 'probe@mail.com'
            user2.set_password('1234')
            user2.save()