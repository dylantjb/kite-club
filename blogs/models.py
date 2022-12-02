from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

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
    bio = models.CharField(max_length = 500, blank = True)
    rules = models.CharField(max_length = 1000, blank = True)
    theme = models.CharField(max_length = 50, blank = True)
