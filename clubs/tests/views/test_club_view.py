from django.test import TestCase
from django.urls import reverse

from clubs.models import Club, User


class ClubPageTest(TestCase):
    fixtures = [
        "clubs/tests/fixtures/default_club.json",
        "clubs/tests/fixtures/other_clubs.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/default_user.json",
    ]

    def setUp(self):
        self.club = Club.objects.get(name="Testing Club")
        self.first_user = User.objects.get(username="@janedoe")
        self.second_user = User.objects.get(username="@adamjohnson")
        self.third_user = User.objects.get(username="@jamesbrown")
        self.club.admins.add(self.first_user)
        self.club.members.add(self.second_user)
        self.club.members.add(self.third_user)
        self.url = reverse("show_club", kwargs={"club_id": self.club.id})

    def test_show_club_url(self):
        self.assertEqual(self.url, f"/club/{self.club.id}")

    def test_get_show_club_with_valid_id(self):
        self.client.login(username=self.first_user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "club_page.html")
        self.assertContains(response, "Testing Club")
        self.assertContains(response, "Comedy")

    def test_get_show_club_with_invalid_id(self):
        self.client.login(username=self.first_user.username, password="Password123")
        url = reverse("show_club", kwargs={"club_id": self.club.id + 9999})
        response = self.client.get(url, follow=True)
        response_url = reverse("club_list")
        self.assertRedirects(
            response, response_url, status_code=302, target_status_code=200
        )
        self.assertTemplateUsed(response, "club_list.html")
