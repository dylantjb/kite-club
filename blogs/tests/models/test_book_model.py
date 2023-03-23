from django.test import TestCase
from django.core.exceptions import ValidationError

from blogs.models import books

class BookModelTestCase(TestCase):
    """Unit tests of the book model"""

    def setUp(self):
        self.books = books.objects.create(
            isbn = "978-0547928202",
            book_title = "The Hobbit",
            book_author = "J.R.R Tolkien",
            year_of_publication = "1937",
            publisher = "Houghton Mifflin Harcourt",
            image_url_s = "http://images.example.org/hobbit_small.jpg",
            image_url_m = "http://images.example.org/hobbit_medium.jpg",
            image_url_l = "http://images.example.org/hobbit_large.jpg"
        )

    def _assert_book_is_valid(self):
        try:
            self.books.full_clean()
        except ValidationError:
            self.fail("Test Book should be valid.")

    def _assert_book_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.books.full_clean()

    def test_book_has_necessary_fields(self):
        self.assertEqual(self.books.isbn, "978-0547928202")
        self.assertEqual(self.books.book_title, "The Hobbit")
        self.assertEqual(self.books.book_author, "J.R.R Tolkien")
        self.assertEqual(self.books.year_of_publication, "1937")
        self.assertEqual(self.books.publisher, "Houghton Mifflin Harcourt")
        self.assertEqual(self.books.image_url_s, "http://images.example.org/hobbit_small.jpg")
        self.assertEqual(self.books.image_url_m, "http://images.example.org/hobbit_medium.jpg")
        self.assertEqual(self.books.image_url_l, "http://images.example.org/hobbit_large.jpg")

    def test_year_of_publication_cannot_exceed_four_digits(self):
        self.books.year_of_publication = "19320"
        self._assert_book_is_invalid()
