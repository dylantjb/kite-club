from django.core.management.base import BaseCommand
import csv
from blogs.models import books

# """ Clear all data and creates addresses """
# MODE_REFRESH = 'refresh'

# """ Clear all data and do not create any object """
# MODE_CLEAR = 'clear'

def process_book_data():
    """ This script opens and then processes the input data from the BX_BOOKS.csv CSV document and returns a list of books. """
    with open('book-review-dataset/BX_Books.csv', encoding='latin-1') as books:
        next(books)
        books_reader = csv.reader(books, delimiter=',')
        #process data in the format of the book model
        book_list = [[book_entry[0],book_entry[1],book_entry[2], book_entry[3],book_entry[4],book_entry[5],book_entry[6],book_entry[7]] for book_entry in books_reader if len(book_entry) > 1 ]
        return book_list
                
class Command(BaseCommand):
    def __init__(self) -> None:
        super().__init__()
        
    def handle(self, *args, **options):
        self.stdout.write('seeding database with books...')
        book_list = process_book_data()
        for book in book_list:
            new_book = books(
                isbn = book[0],
                book_title = book[1],
                book_author = book[2],
                year_of_publication = book[3],
                publisher = book[4],
                image_url_s = book[5],
                image_url_m = book[6],
                image_url_l = book[7],
            )
            new_book.save()
        self.stdout.write('done.')
