"""Unit tests for the Club form"""
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from blogs.forms import CreateClubForm
from blogs.models import User, Club

# Not finished - may need to test views create_club method directly
class ClubFormTestCase(TestCase):
    """Unit tests of the club form."""

    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Test',
            last_name='Smith',
            username='@testsmith',
            email='testsmith@example.org' ,
            bio='hello',
            password='12345')
        self.client = Client()
        self.logged_in_user = self.client.login(username='@testsmith',password='12345')

        self.form = CreateClubForm(data = {'name' : 'testclub'})
        self.club = self.form.save()

        # this part is what is done by the create_club method in views.py
        self.club.admins.add(self.user)
        self.club.members.add(self.user)

    def test_user_logged_in(self):
        self.assertTrue(self.logged_in_user)

    def test_logged_in_user_is_admin_of_created_club(self):
        self.assertTrue(self.club in self.user.admin_of.all())
        self.assertTrue(self.user in self.club.admins.all())
