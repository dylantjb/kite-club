from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from blogs.forms import SignUpForm
from blogs.models import User

class SignUpFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 
        }
