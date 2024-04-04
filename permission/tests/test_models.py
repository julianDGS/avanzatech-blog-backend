from datetime import datetime
from django.test import TestCase
from django.db import IntegrityError

from ..models import Permission, PermissionName
# from .factories.permission_factories import *

class PermissionTest(TestCase):

    def test_permission_exist(self):
        permission = Permission.objects.all()

        self.assertEqual(permission.count(), 0)

    def test_create_new_read_permission(self):        
        permission = Permission(name=PermissionName.READ)
        permission.save()
        created_date = datetime.now().date()
        
        permissions_from_db = Permission.objects.all()
        self.assertEqual(len(permissions_from_db), 1)
        
        permission_created = permissions_from_db[0]
        self.assertEqual(PermissionName.READ, permission_created.name)
        self.assertTrue(permission.id)
        self.assertEqual(permission_created.created_at, permission_created.updated_at.date())
        self.assertEqual(permission_created.created_at, created_date)
    
    def test_create_new_edit_permission(self):        
        permission = Permission(name=PermissionName.EDIT)
        permission.save()
        created_date = datetime.now().date()
        
        permissions_from_db = Permission.objects.all()
        self.assertEqual(len(permissions_from_db), 1)
        
        permission_created = permissions_from_db[0]
        self.assertEqual(PermissionName.EDIT, permission_created.name)
        self.assertTrue(permission.id)
        self.assertEqual(permission_created.created_at, permission_created.updated_at.date())
        self.assertEqual(permission_created.created_at, created_date)

    def test_validate_required_fields(self):
        with self.assertRaises(IntegrityError):
            permission = Permission()
            permission.save()


    