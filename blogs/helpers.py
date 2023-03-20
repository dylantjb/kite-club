from django.conf import settings
from django.shortcuts import redirect


def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        return view_function(request)

    return modified_view_function


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
