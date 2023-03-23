from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from libgravatar import Gravatar

from .helpers import get_genres, get_themes

class User(AbstractUser):
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
    favourite_genre = models.CharField(max_length = 2, choices = get_genres(), default="NO")

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


class Book(models.Model):
    isbn = models.CharField(_("ISBN"),max_length=255)
    book_title = models.CharField(_("Book-Title"),max_length=255)
    book_author = models.CharField(_("Book-Author"),max_length=255)
    year_of_publication = models.CharField(_("Year-Of-Publication"),max_length=4)
    publisher = models.CharField(_("Publisher"),max_length=255)
    image_url_s = models.CharField(_("Image-URL-S"),max_length=255)
    image_url_m = models.CharField(_("Image-URL-M"),max_length=255)
    image_url_l = models.CharField(_("Image-URL-L"),max_length=255)
    
class FeaturedBook(models.Model):
    book_title = models.CharField(max_length=255, blank=False)
    book_author = models.CharField(max_length=255, blank=False)
    curator = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)

    
class Club(models.Model):
    admins = models.ManyToManyField(User, related_name='admin_of', blank=False)
    members = models.ManyToManyField(User, related_name='member_of', blank=False)
    pending_members = models.ManyToManyField(User, related_name='pending_member_of', blank=True)
    name = models.CharField(
        max_length = 50,
        validators = [RegexValidator(
            regex = r'^[a-zA-Z]*$',
            message = 'Club name cannot contain numbers and special characters in their name.'
        )]
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name = 'owned_clubs')
    bio = models.CharField(max_length = 500, blank = True)
    rules = models.CharField(max_length = 1000, blank = True)
    theme = models.CharField(max_length = 2, choices = get_themes(), blank=False, default="")
    book = models.ForeignKey(FeaturedBook, on_delete=models.CASCADE, null=True, blank=True)

    
class Post(models.Model):
    """Posts by users in a given club."""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    in_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='club_posts')

    class Meta:
        """Model options."""

        ordering = ['-created_at']

class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length = 280)
    created_at = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='upcoming_events')
    title = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField(max_length=1024, blank=False)
    location = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=50, blank=True)
    date = models.DateField(blank=False)
    startTime = models.TimeField(blank=False)
    endTime = models.TimeField()
    eventLink = models.CharField(max_length=200, blank=True)
    selectedBook = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="club_events", blank=True, null=True)
    attendees = models.ManyToManyField (
        User,
        through='AttendEvent',
        through_fields=('event', 'user'),
        related_name='upcoming_events'
    )

class AttendEvent(models.Model):
    class Meta:
        unique_together = ('event', 'user')

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attend_event')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attend_event')
