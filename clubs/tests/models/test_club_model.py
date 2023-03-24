"""Unit tests for the Club model"""
from django.core.exceptions import ValidationError
from django.test import TestCase

from clubs.helpers import get_themes
from clubs.models import Club, FeaturedBook, User


class ClubModelTestCase(TestCase):
    """Unit tests for the club model"""

    def setUp(self):
        self.user = User.objects.create(
            username="@johnsmith",
            first_name="John",
            last_name="Smith",
            email="johnsmith@example.org",
            password="Password123",
            bio="Hi I am John Smith",
            favourite_genre="T",
        )

        user_jane_smith = User.objects.create(
            username="@janesmith",
            first_name="Jane",
            last_name="Smith",
            email="janesmith@example.org",
            bio="Hi I am Jane Smith",
            favourite_genre="RO",
        )

        user_michael_doe = User.objects.create(
            username="@michaeldoe",
            first_name="Michael",
            last_name="Doe",
            email="michaeldoe@example.org",
            bio="Hi I am Michael Doe here!",
            favourite_genre="P",
        )

        self.club = Club.objects.create(
            name="Test Club", owner=self.user, theme="T", book=None
        )

        Club.objects.create(
            name="Test Club 2", owner=user_jane_smith, theme="RO", book=None
        )

        Club.objects.create(
            name="Test Club 3", owner=user_michael_doe, theme="P", book=None
        )

    def test_club_has_been_created_correctly(self):
        club = Club.objects.create(name="Test Club", owner=self.user, theme="T")
        self.assertTrue(isinstance(club, Club))

    def test_club_name_cannot_contain_numbers_or_special_characters(self):
        with self.assertRaises(ValidationError):
            club = Club.objects.create(name="Test Club #1", owner=self.user, theme="T")
            club.full_clean()

    def test_club_featured_book_is_assigned(self):
        club = self.club
        book = FeaturedBook.objects.create(
            book_title="Test Book", book_author="Test Author", curator=self.user
        )
        club.book = book
        club.save()
        self.assertEqual(club.book, book)

    def test_club_can_add_members(self):
        club = self.club
        user = User.objects.create(
            username="@testuser",
            first_name="Test",
            last_name="User",
            email="testuser1@example.org",
            password="Password123",
            bio="Hi I am Test User",
            favourite_genre="T",
        )
        club.members.add(user)
        self.assertIn(user, club.members.all())

    def test_club_can_add_admins(self):
        club = self.club
        user = User.objects.create(
            username="@testuser",
            first_name="Test",
            last_name="User",
            email="testuser1@example.org",
            password="Password123",
            bio="Hi I am Test User",
            favourite_genre="T",
        )
        club.admins.add(user)
        self.assertIn(user, club.admins.all())

    def test_clubs_can_have_pending_members(self):
        club = self.club
        user = User.objects.create(
            username="@testuser",
            first_name="Test",
            last_name="User",
            email="testuser1@example.org",
            password="Password123",
            bio="Hi I am Test User",
            favourite_genre="T",
        )
        club.pending_members.add(user)
        self.assertIn(user, club.pending_members.all())
