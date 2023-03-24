import csv
import heapq
from collections import defaultdict
from operator import itemgetter
from pathlib import Path

from surprise import Dataset, KNNBaseline, Reader


# Load in the book ratings and return a dataset.
def load_dataset():
    print("Loading book ratings...")
    reader = Reader(line_format="user item rating", sep=",", skip_lines=1)
    ratings_dataset = Dataset.load_from_file(
        Path("book-review-dataset/top_ratings.csv"), reader=reader
    )

    # Lookup a book's name with it's ISBN/BookID as key
    bookID_to_name = {}
    with open(
        Path("book-review-dataset/BX_Books.csv"), newline="", encoding="ISO-8859-1"
    ) as csvfile:
        book_reader = csv.reader(csvfile)
        next(book_reader)
        for row in book_reader:
            bookID = row[0]
            book_name = row[1]
            bookID_to_name[bookID] = book_name
    # Return both the dataset and lookup dict in tuple
    return (ratings_dataset, bookID_to_name)


data, bookID_to_name = load_dataset()
print("\nBuilding recommendation model, this may take a few seconds...")
# Build training set from the data
trainset = data.build_full_trainset()

similarity_matrix = (
    KNNBaseline(sim_options={"name": "pearson", "user_based": False})
    .fit(trainset)
    .compute_similarities()
)

# Pick a random user ID
test_subject = "276747"

# Get the top K items user rated
k = 20

test_subject_iid = trainset.to_inner_uid(test_subject)

# Get the top K items we rated
test_subject_ratings = trainset.ur[test_subject_iid]
k_neighbors = heapq.nlargest(k, test_subject_ratings, key=lambda t: t[1])

# Default dict is basically a standard dictionary,
# the difference beeing that it doesn't throw an error
# when trying to access a key which does not exist,
# instead a new entry, with that key, is created.
candidates = defaultdict(float)

for itemID, rating in k_neighbors:
    try:
        similaritities = similarity_matrix[itemID]
        for innerID, score in enumerate(similaritities):
            candidates[innerID] += score * (rating / 5.0)
    except:
        continue


# Utility we'll use later.
def getBookName(bookID):
    if (bookID) in bookID_to_name:
        return bookID_to_name[(bookID)]
    else:
        return ""


# Build a dictionary of books the user has read
read = {}
for itemID, rating in trainset.ur[test_subject_iid]:
    read[itemID] = 1

# Add items to list of user's recommendations
# If they are similar to their favorite books,
# AND have not already been read.
recommendations = []

position = 0
for itemID, rating_sum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
    if not itemID in read:
        recommendations.append(getBookName(trainset.to_raw_iid(itemID)))
        position += 1
        if position > 9:
            break  # We only want top 10
print("\nBooks we recommend:")
for rec in recommendations:
    print(rec)
