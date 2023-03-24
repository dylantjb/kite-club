from django.conf import settings
from django.shortcuts import redirect

from .models import Book, Club

from random import randint



"""----------------------------HELPER FUNCTIONS----------------------------------"""

def get_genres():
    return [  # Taken from Google Books
        ("NO", "None"),
        ("E", "Ebooks"),
        ("A", "Arts"),
        ("BM", "Biographies & Memoirs"),
        ("BI", "Business & Investing"),
        ("C", "Comics"),
        ("CT", "Computers & Technology"),
        ("CF", "Cookery, Food & Wine"),
        ("F", "Fantasy"),
        ("FL", "Fiction & Literature"),
        ("G", "Gardening"),
        ("HF", "Health & Fitness"),
        ("HM", "Health, Mind & Body"),
        ("H", "History"),
        ("M", "Mystery & Thrillers"),
        ("N", "Nature"),
        ("P", "Poetry"),
        ("PC", "Politics & Current Affairs"),
        ("R", "Reference"),
        ("RO", "Romance"),
        ("RS", "Religion & Spirituality"),
        ("S", "Science"),
        ("SF", "Science Fiction"),
        ("SP", "Sports"),
        ("T", "Travel"),
        ("Y", "Young Adult"),
    ]


def get_themes():
    return get_genres()[1:]

def active_count(club):
    count = 0
    for user in club.members.all():
        if user.is_active:
            count+=1
    return count


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


def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        return view_function(request)

    return modified_view_function