"""Unit tests for the User model"""
from django.core.exceptions import ValidationError
from django.test import TestCase

from blogs.helpers import get_themes
from blogs.models import User


class UserModelTestCase(TestCase):
    """Unit tests of the user model."""

    fixtures = [
        "blogs/tests/fixtures/default_user.json",
        "blogs/tests/fixtures/other_users.json",
    ]

    def setUp(self):
        self.user = User.objects.get(username="@johnsmith")

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except ValidationError:
            self.fail("Test user should be valid")

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_username_must_have_at_least_three_alphanumericals(self):
        """Test username must have at least three alphanumericals."""
        self.user.username = "ab"
        self._assert_user_is_invalid()

    def test_username_cannot_be_blank(self):
        """Test username cannot be blank."""
        self.user.username = ""
        self._assert_user_is_invalid()

    def test_username_can_be_30_characters_long(self):
        """Test username can be 30 characters long."""
        self.user.username = "@" + "x" * 29
        self._assert_user_is_valid()

    def test_username_cannot_be_over_30_characters_long(self):
        """Test username cannot be over 30 characters long."""
        self.user.username = "@" + "x" * 30
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        """Test username must be unique."""
        second_user = User.objects.get(username="@janedoe")
        self.user.username = second_user.username
        self._assert_user_is_invalid()

    def test_username_has_numbers(self):
        """Test username has numbers."""
        self.user.username = "@j0hnd03"
        self._assert_user_is_valid()

    def test_username_is_case_insensitive(self):
        """Test user is case insensitive."""
        second_user = User.objects.get(username="@janedoe")
        self.user.username = second_user.username.upper()
        self._assert_user_is_valid()

    def test_first_name_is_not_blank(self):
        """Test first name must not be blank."""
        self.user.first_name = ""
        self._assert_user_is_invalid()

    def test_first_name_is_not_unique(self):
        """Test first name is not unique."""
        second_user = User.objects.get(username="@janedoe")
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_can_have_less_than_50_characters(self):
        """Test first name can have less than 50 characters."""
        self.user.first_name = "x" * 50
        self._assert_user_is_valid()

    def test_first_name_cannot_have_more_than_50_characters(self):
        """Test first name cannot have more than 50 characters."""
        self.user.first_name = "x" * 51
        self._assert_user_is_invalid()

    def test_last_name_is_not_blank(self):
        """Test last name is not blank."""
        self.user.last_name = ""
        self._assert_user_is_invalid()

    def test_last_name_is_not_unique(self):
        """Test last name is not unique."""
        second_user = User.objects.get(username="@janedoe")
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_last_name_can_have_less_than_50_characters(self):
        """Test last name can have less than 50 characters."""
        self.user.last_name = "x" * 50
        self._assert_user_is_valid()

    def test_last_name_cannot_have_more_than_50_characters(self):
        """Test last name cannot have more than 50 characters."""
        self.user.last_name = "x" * 51
        self._assert_user_is_invalid()

    def test_email_must_not_be_blank(self):
        """Test email must not be blank."""
        self.user.email = ""
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        """Test email must contain a domain name."""
        self.user.email = "johndoe@example"
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        """Test email must not contain more than one @"""
        self.user.email = "johndoe@@example.org"
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        """Test email must contain @."""
        self.user.email = "johndoe.example.org"
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        """Test email must be unique."""
        second_user = User.objects.get(username="@janedoe")
        self.user.email = second_user.email
        self._assert_user_is_invalid()

    def test_email_is_not_case_sensitive(self):
        """Test email is not case sensitive."""
        second_user = User.objects.get(username="@janedoe")
        self.user.email = second_user.email.upper()
        self._assert_user_is_invalid()

    def test_favourite_genre_can_be_blank(self):
        """Test genre can be blank."""
        self.user.favourite_genre = ""
        self._assert_user_is_valid()

    def test_valid_favourite_genre(self):
        """Test all favourite genres."""
        for i in [j[0] for j in get_themes()[0]]:
            self.user.favourite_genre = i
            self._assert_user_is_valid()

    def test_bio_can_be_blank(self):
        """Test bio can be blank."""
        self.user.bio = ""
        self._assert_user_is_valid()

    def test_bio_may_not_be_unique(self):
        """Test bio may not be unique."""
        second_user = User.objects.get(username="@janedoe")
        self.user.bio = second_user.bio
        self._assert_user_is_valid()

    def test_bio_may_have_520_chars(self):
        """Test bio may have 520 characters."""
        self.user.bio = "x" * 520
        self._assert_user_is_valid()

    def test_bio_cannot_have_over_520_chars(self):
        """Test bio cannot have over 520 characters."""
        self.user.bio = "x" * 521
        self._assert_user_is_invalid()

    def test_bio_may_contain_numbers(self):
        """Test bio may contain numbers."""
        self.user.bio = "bio 2"
        self._assert_user_is_valid()
