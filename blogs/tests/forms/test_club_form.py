"""Unit tests for the Club form"""
from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from blogs.forms import CreateClubForm
from blogs.models import User, Club

# Not finished - may need to test views create_club method directly
class ClubFormTestCase(TestCase):
    """Unit tests of the club form."""

    fixtures = [
        "blogs/tests/fixtures/default_user.json"
    ]

    def setUp(self):
        self.user = User.objects.get(username = '@johnsmith')
        self.club = Club.objects.create(
            name = "Club XL",
            owner = self.user,
            theme = "Literature",
            bio = "Literature fans wanted",
            rules = "Do not flame!"
        )
        self.client = Client()
        self.logged_in_user = self.client.login(username='@johnsmith',password='pbkdf2_sha256$260000$4BNvFuAWoTT1XVU8D6hCay$KqDCG+bHl8TwYcvA60SGhOMluAheVOnF1PMz0wClilc=')

        self.form_input = {
            "name": "Club XL",
            "owner": self.user,
            "theme": "Horror",
            "bio": "The club where all can talk about horror books",
            "rules": "Be Nice"
        }

        # this part is what is done by the create_club method in views.py
        self.club.admins.add(self.user)
        self.club.members.add(self.user)

    def test_user_logged_in(self):
        self.assertTrue(self.logged_in_user)

    def test_logged_in_user_is_admin_of_created_club(self):
        self.assertTrue(self.club in self.user.admin_of.all())
        self.assertTrue(self.user in self.club.admins.all())

    def test_valid_club_form(self):
        form = CreateClubForm(data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_create_club_form_has_necessary_fields(self):
        form = CreateClubForm()
        self.assertIn('name', form.fields)

        club_field = form.fields['name']
        self.assertTrue(isinstance(club_field, forms.CharField))

    def test_form_has_model_validation(self):
        self.form_input['name'] = None
        form = CreateClubForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_cannot_create_two_clubs_with_the_same_name(self):
        self.form_input['name'] = "Book Club"
        form = CreateClubForm(data = self.form_input)
        self.assertFalse(form.is_valid())
