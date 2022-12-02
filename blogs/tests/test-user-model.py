"""Unit tests for the User model"""
from django.core.exceptions import ValidationError
from django.test import TestCase

from blogs.models import User


class UserModelTestCase(TestCase):
    """Unit tests of the user model."""

    fixtures = [
        "blogs/tests/fixtures/default_user.json",
        "blogs/tests/fixtures/other_users.json",
    ]

    def setUp(self):
        self.user = User.objects.get(username="johnsmith")

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
        self.user.username = "x" * 30
        self._assert_user_is_valid()

    def test_username_cannot_be_over_30_characters_long(self):
        """Test username cannot be over 30 characters long."""
        self.user.username = "x" * 31
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        """Test username must be unique."""
        second_user = User.objects.get(username="janedoe")
        self.user.username = second_user.username
        self._assert_user_is_invalid()

    def test_username_has_numbers(self):
        """Test username has numbers."""
        self.user.username = "j0hnd03"
        self._assert_user_is_valid()

    def test_first_name_is_not_blank(self):
        """Test first name must not be blank."""
        self.user.first_name = ""
        self._assert_user_is_invalid()

    def test_first_name_is_not_unique(self):
        """Test first name is not unique."""
        second_user = User.objects.get(username="janedoe")
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
        second_user = User.objects.get(username="janedoe")
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

    def test_bio_can_be_blank(self):
        """Test bio can be blank."""
        self.user.bio = ""
        self._assert_user_is_valid()

    def test_bio_may_not_be_unique(self):
        """Test bio may not be unique."""
        second_user = User.objects.get(username="janedoe")
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
