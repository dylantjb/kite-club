from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower
from django.utils.translation import gettext as _
from libgravatar import Gravatar

from .helpers import get_genres, get_themes

class User(AbstractUser):
    def _init_(self):
        self.members = []
        self.admins = []
        self.genres = []
        self.themes = []
        self.visibility = "private"

    def invite_member(self, member):
        if member in self.members:
            print(f"Error: {member} is already a member of the club.")
        else:
            self.members.append(member)
            print(f"{member} has been invited to the club.")

    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)
            print(f"{member} has been removed from the club.")
        else:
            print(f"Error: {member} is not a member of the club.")

    def set_admin(self, member):
        if member in self.members:
            self.admins.append(member)
            print(f"{member} has been set as an admin of the club.")
        else:
            print(f"Error: {member} is not a member of the club.")

    def remove_admin(self, member):
        if member in self.admins:
            self.admins.remove(member)
            print(f"{member} has been removed as an admin of the club.")
        else:
            print(f"Error: {member} is not an admin of the club.")

    def add_genre(self, genre):
        self.genres.append(genre)
        print(f"{genre} has been added as a genre of the club.")

    def remove_genre(self, genre):
        if genre in self.genres:
            self.genres.remove(genre)
            print(f"{genre} has been removed as a genre of the club.")
        else:
            print(f"Error: {genre} is not a genre of the club.")

    def add_theme(self, theme):
        self.themes.append(theme)
        print(f"{theme} has been added as a theme of the club.")

    def remove_theme(self, theme):
        if theme in self.themes:
            self.themes.remove(theme)
            print(f"{theme} has been removed as a theme of the club.")
        else:
            print(f"Error: {theme} is not a theme of the club.")

    def set_visibility(self, visibility):
        if visibility in ["private", "public"]:
            self.visibility = visibility
            print(f"The club visibility has been set to {visibility}.")
        else:
            print("Error: Visibility can only be set to 'private' or 'public'.")

    def close_club(self):
        self.members = []
        self.admins = []
        self.genres = []
        self.themes = []
        self.visibility = "private"
        print("The club has been closed.")

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length = 50, blank = False)
    last_name = models.CharField(max_length = 50, blank = False)
    email = models.EmailField(unique = True, blank = False)
    bio = models.CharField(max_length = 520, blank = True)
    favourite_genre = models.CharField(max_length = 2, choices = get_genres(), default=("NO", "None"))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                name="unique_lower_user_email",
            )
        ]

    def gravatar(self, size=120):
        return Gravatar(self.email).get_image(size=size, default='mp')
    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=60)
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Club(models.Model):
    admins = models.ManyToManyField(User, related_name='admin_of', blank=False)
    members = models.ManyToManyField(User, related_name='member_of', blank=False)
    pending_members = models.ManyToManyField(User, related_name='pending_member_of', blank=True)
    name = models.CharField(
        max_length = 50,
        validators = [RegexValidator(
            regex = r'^\w{3,}$',
            message = 'Club name must consist of at least 3 alphanumericals.'
        )]
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name = 'owned_clubs')
    bio = models.CharField(max_length = 500, blank = True)
    rules = models.CharField(max_length = 1000, blank = True)
    theme = models.CharField(max_length = 2, choices = get_genres(), default=("NO", "None"))

class Post(models.Model):
    """Posts by users in a given club."""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    in_club = models.ForeignKey(Club, on_delete=models.CASCADE)

    class Meta:
        """Model options."""

        ordering = ['-created_at']



class books(models.Model):
    isbn = models.CharField(_("ISBN"),max_length=255)
    book_title = models.CharField(_("Book-Title"),max_length=255)
    book_author = models.CharField(_("Book-Author"),max_length=255)
    year_of_publication = models.IntegerField(_("Year-Of-Publication"))
    publisher = models.CharField(_("Publisher"),max_length=255)
    image_url_s = models.CharField(_("Image-URL-S"),max_length=255)
    image_url_m = models.CharField(_("Image-URL-M"),max_length=255)
    image_url_l = models.CharField(_("Image-URL-L"),max_length=255)
