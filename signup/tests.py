from datetime import datetime
from django.test import Client, TestCase
import pytz

from accounts.models import PS1User
from member_management.models import Person

from .forms import activate_account_form, account_register_form
from .models import Token
from pprint import pprint


class ActivationTest(TestCase):
    def setUp(self):
        self.person = Person(
                    first_name = "Jay",
                    last_name="Hacker",
                    email="J.R.Hacker@example.com",
                    membership_status="Starving",
                    )
        self.person.save()

    def tearDown(self):
        self.person.delete()

    def get_token(self):
        return Token.objects.get(person = self.person)

    def test_activation_form(self):

        activation_data = {}
        activation_data['ps1_email'] = "J.R.Hacker@example.com"
        activation_form = activate_account_form(data = activation_data)
        self.assertTrue(activation_form.is_valid())
        activation_form.save(use_https = False, domain = "example.com")
        
        #an email gets sent out. since I don't know how to retrieve it, I am going to cheat
        self.token = Token.objects.get(person = self.person);
        self.assertIsNotNone(self.token)

    def test_register_form(self):
        """
        This tests most of the zoho activation path.
        """
        activation_data = {}
        activation_data['ps1_email'] = "J.R.Hacker@example.com"
        activation_form = activate_account_form(data = activation_data)
        self.assertTrue(activation_form.is_valid())
        activation_form.save(use_https = False, domain = "example.com")
        
        #an email gets sent out. since I don't know how to retrieve it, I am going to cheat
        self.token = Token.objects.get(person = self.person);
        self.assertIsNotNone(self.token)
        register_data = {}
        register_data['token'] = self.token.token
        register_data['preferred_username'] = 'jrhacker'
        register_data['first_name'] = 'Jay'
        register_data['last_name'] = 'Hacker'
        register_data['preferred_email'] = 'J.R.Hacker@example.com'
        register_form = account_register_form(data=register_data)
        self.assertTrue(register_form.is_valid())
        user = register_form.save()
        self.assertIsNotNone(user)
        
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(person = self.person)
        
        PS1User.objects.delete_user(user)

    def test_activate(self):
        c = Client()

        response = c.get('/signup/activate/')
        self.assertEqual(response.status_code, 200)

        response = c.post('/signup/activate/', {'ps1_email': 'J.R.Hacker@example.com'}, follow=True)
        self.assertEqual(response.status_code, 200)

        # "read" email
        token = self.get_token()
        activation_url = '/signup/activate/confirm/{}'.format(token.token)
        response = c.get(activation_url)
        self.assertEqual(response.status_code, 200)
        
        post_data = {
            'preferred_username': 'jay',
            'first_name': 'Jay',
            'last_name': 'Hacker',
            'preferred_email': 'J.R.Hacker@example.com',
            'token': token.token,
        }
        response = c.post(activation_url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)

        jay = Person.objects.get(pk=self.person.pk)
        self.assertIsNotNone(jay.user)
        PS1User.objects.delete_user(jay.user)
