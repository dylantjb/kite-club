"""Unit tests for the Club model"""
from django.core.exceptions import ValidationError
from django.test import TestCase

from blogs.models import Club
from blogs.helpers import get_themes

class ClubModelTestCase(TestCase):
  """ Unit tests for the club model"""

  fixtures = [
    "blogs/tests/fixtures/default_club.json",
    "blogs/tests/fixtures/other_clubs.json"
  ]

  def setUp(self):
      self.club = Club.objects.get(name = "Testing Club")

  def _assert_club_is_valid(self):
      try:
          self.club.full_clean()
      except ValidationError:
          self.fail("Test Club should be valid.")

  def _assert_club_is_invalid(self):
      with self.assertRaises(ValidationError):
          self.club.full_clean()

  def test_club_name_cannot_be_blank(self):
      """Test clubname cannot be blank."""
      self.club.name = ""
      self._assert_club_is_invalid()

  def test_club_name_can_be_30_characters_long(self):
      """Test club name can be 30 characters long."""
      self.club.name = "@" + "x" * 29
      self._assert_club_is_valid()

  def test_club_name_cannot_be_over_30_characters_long(self):
      """Test club name cannot be over 30 characters long."""
      self.club.name = "x" * 31
      self._assert_club_is_invalid()

  def test_club_bio_can_be_520_characters_long(self):
      """Test club bio can be 520 characters long."""
      self.club.bio = "x" * 520
      self._assert_club_is_valid()

  def test_club_bio_cannot_be_over_520_characters_long(self):
      """Test club bio cannot be over 520 characters long."""
      self.club.bio = "x" * 521
      self._assert_club_is_invalid()

  def test_club_name_cannot_contain_numbers(self):
      """Test club cannot contain numbers."""
      self.club.name = "bio 2"
      self._assert_club_is_invalid()

  def test_club_name_cannot_contain_special_characters(self):
      """Test club name cannot contain any special characters."""
      self.club.name = "bio-"
      self._assert_club_is_invalid()

  def test_club_bio_can_be_blank(self):
      """Test club bio can be blank."""
      self.club.bio = ""
      self._assert_club_is_valid()

  def test_club_rules_can_be_blank(self):
      """Test club rules can be blank."""
      self.club.rules = ""
      self._assert_club_is_valid()

  def test_club_name_must_be_unique(self):
      """Test club name must be unique."""
      second_club = Club.objects.get(name = "Other Club")
      self.club.name = second_club.name
      self._assert_club_is_invalid()
