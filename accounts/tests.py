from django.test import TestCase
from .models import PS1User
from ldap3 import Server, Connection, SUBTREE, Tls, MODIFY_REPLACE, BASE, ALL_ATTRIBUTES
from django.conf import settings
from django.test import Client
from pprint import pprint
import uuid


class AccountTest(TestCase):

    def setUp(self):
        pass

    def test_create_user(self):
        user = PS1User.objects.create_user("testuser", password="Garbage1",  email="foo@bar.com")
        self.assertEqual(user.get_short_name(), 'testuser')
        self.assertTrue(user.has_usable_password())
        self.assertTrue(user.check_password('Garbage1'))
        self.assertFalse(user.check_password('wrong_password'))
        self.assertEqual("foo@bar.com", user.ldap_user['mail'][0])
        self.assertFalse(user.is_staff)
        PS1User.objects.delete_user(user)

    def test_create_superuser(self):
        user = PS1User.objects.create_superuser("superuser", email='super@user.com', password='Garbage2')
        self.assertTrue(user.is_staff)
        PS1User.objects.delete_user(user)


    def test_login(self):
        user = PS1User.objects.create_user("testuser", password="Garbage1",  email="foo@bar.com")
        c = Client()
        result = c.login(username='testuser', password='Garbage1')
        self.assertTrue(result)
        PS1User.objects.delete_user(user)


