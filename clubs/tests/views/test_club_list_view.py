from django.test import TestCase
from django.urls import reverse

from clubs.models import Club, User


class ClubListTest(TestCase):
    fixtures = [
        "clubs/tests/fixtures/default_club.json",
        "clubs/tests/fixtures/other_clubs.json",
        "clubs/tests/fixtures/other_users.json",
    ]

    # do we need the super class call?
    def setUp(self):
        self.url = reverse("club_list")
        self.club = Club.objects.get(name="Testing Club")
        self.first_user = User.objects.get(username="@janedoe")
        self.second_user = User.objects.get(username="@adamjohnson")
        self.third_user = User.objects.get(username="@jamesbrown")
        self.club.admins.add(self.first_user)
        self.club.members.add(self.second_user)
        self.club.members.add(self.third_user)

    def test_club_list_url(self):
        self.assertEqual(self.url, "/clubs/")

    def test_get_club_list(self):
        self.client.login(username=self.first_user.username, password="Password123")
        other_club = Club.objects.get(name="Other Club")
        other_club.admins.add(self.second_user)
        other_club.members.add(self.first_user)
        other_club.members.add(self.third_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "club_list.html")
        self.assertContains(response, self.club.name)
        self.assertContains(response, self.club.theme)
        # self.assertContains(response, self.club.bio)
        self.assertContains(response, other_club.name)
        self.assertContains(response, other_club.theme)
        # self.assertContains(response, other_club.bio)
