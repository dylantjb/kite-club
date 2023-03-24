import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from surprise import Dataset, Reader


class BookData:
    bookID_to_name = {}
    name_to_bookID = {}

    booksPath = Path("book-review-dataset/BX_Books.csv")
    ratingsPath = Path("book-review-dataset/top_ratings.csv")

    def loadBookData(self):
        # Look for files relative to the directory we are running from
        ratingsDataset = 0
        self.bookID_to_name = {}
        self.name_to_bookID = {}

        reader = Reader(line_format="user item rating", sep=",", skip_lines=1)

        ratingsDataset = Dataset.load_from_file(BookData.ratingsPath, reader=reader)

        with open(self.booksPath, newline="", encoding="ISO-8859-1") as csvfile:
            bookReader = csv.reader(csvfile)
            next(bookReader)  # Skip header line
            for row in bookReader:
                bookID = row[0]
                bookName = row[1]
                self.bookID_to_name[bookID] = bookName
                self.name_to_bookID[bookName] = bookID

        return ratingsDataset

    def getUserRatings(self, user):
        userRatings = []
        hitUser = False
        with open(self.ratingsPath, newline="") as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                userID = int(row[0])
                if user == userID:
                    bookID = row[1]
                    rating = float(row[2])
                    userRatings.append((bookID, rating))
                    hitUser = True
                if hitUser and (user != userID):
                    break

        return userRatings

    def getBookName(self, bookID):
        if bookID in self.bookID_to_name:
            return self.bookID_to_name[bookID]
        else:
            return ""

    def getBookID(self, bookName):
        if bookName in self.name_to_bookID:
            return self.name_to_bookID[bookName]
        else:
            return 0
