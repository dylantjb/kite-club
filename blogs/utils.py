from .models import Book, Club
from random import randint

"""SETUP and UTILITARY functions for views"""

def pending_requests_count(user):
    pending = []
    for club in Club.objects.all():
        if user in (club.owner, club.admins.all()):
            pending.extend(club.pending_members.all())
    return len(pending)

def get_top_picks(feed_books=[]):
    if Book.objects.all():
        count = Book.objects.count()
        for i in range(0,2):
            feed_books.append(Book.objects.all()[randint(0, count - 1)])
    return feed_books