import pandas as pd
import numpy as np


import matplotlib.pyplot as plt
from string import ascii_letters, digits
from surprise.model_selection import cross_validate


def pre_process():
        books = pd.read_csv('data/BX_Books.csv', sep=';', error_bad_lines=False, encoding="latin-1")
        books.columns = ['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-S', 'Image-URL-M', 'Image-URL-L']
        users = pd.read_csv('data/BX-Users.csv', sep=';', error_bad_lines=False, encoding="latin-1")
        users.columns = ['User-ID', 'Location', 'Age']
        ratings = pd.read_csv('data/BX-Book-Ratings.csv', sep=';', error_bad_lines=False, encoding="latin-1")
        ratings.columns = ['User-ID', 'ISBN', 'Book_Rating']

        users.columns = users.columns.str.strip().str.lower().str.replace('-', '_')
        books.columns = books.columns.str.strip().str.lower().str.replace('-', '_')   
        books.drop(columns=['image_url_s', 'image_url_m', 'image_url_l'], inplace=True)
        ratings.columns = ratings.columns.str.strip().str.lower().str.replace('-', '_')

        ratings_explicit = ratings[ratings['book_rating']!=0]
        ratings_implicit = ratings[ratings['book_rating']==0]

        counts1 = ratings['user_id'].value_counts()
        ratings = ratings[ratings['user_id'].isin(counts1[counts1 >= 200].index)]
        counts = ratings['book_rating'].value_counts()
        ratings = ratings[ratings['book_rating'].isin(counts[counts >= 100].index)]

        user_ratings_threshold = 3

        filter_users = ratings_explicit['user_id'].value_counts()
        filter_users_list = filter_users[filter_users >= user_ratings_threshold].index.to_list()

        df_ratings_top = ratings_explicit[ratings_explicit['user_id'].isin(filter_users_list)]

        print('Filter: users with at least %d ratings\nNumber of records: %d' % (user_ratings_threshold, len(df_ratings_top)))

        book_ratings_threshold_perc = 0.1
        book_ratings_threshold = len(df_ratings_top['isbn'].unique()) * book_ratings_threshold_perc

        filter_books_list = df_ratings_top['isbn'].value_counts().head(int(book_ratings_threshold)).index.to_list()
        df_ratings_top = df_ratings_top[df_ratings_top['isbn'].isin(filter_books_list)]

        print('Filter: top %d%% most frequently rated books\nNumber of records: %d' % (book_ratings_threshold_perc*100, len(df_ratings_top)))

        df_ratings_top.to_csv('data/top_ratings.csv', encoding='utf-8', index=False)