"""Tests for the log in view"""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse

from clubs.forms import LogInForm
from clubs.models import User
from clubs.tests.helpers import LogInTester


class LogInViewTestCase(TestCase, LogInTester):
    fixtures = ["clubs/tests/fixtures/default_user.json"]

    def setUp(self):
        self.url = reverse("log_in")
        self.user = User.objects.get(username="@johnsmith")

    def test_log_in_url(self):
        self.assertEqual(self.url, "/log_in/")

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "log_in.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_log_in(self):
        form_input = {"username": "@johnsmith", "password": "WrongPassword123"}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "log_in.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_successful_log_in(self):
        form_input = {"username": "@johnsmith", "password": "Password123"}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse("feed")
        self.assertRedirects(
            response, response_url, status_code=302, target_status_code=200
        )
        self.assertTemplateUsed(response, "feed.html")
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 0)
