import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

from surprise import Dataset, Reader
from surprise import KNNBasic, KNNWithMeans, KNNWithZScore, KNNBaseline
from surprise.model_selection import cross_validate, train_test_split, GridSearchCV




def get_model_name(model):
    return str(model).split('.')[-1].split(' ')[0].replace("'>", "")


def cv_multiple_models(data, models_dict, cv=3):
    results = pd.DataFrame()

    for model_name, model in models_dict.items():
        print('\n---> CV for %s...' % model_name)

        cv_results = cross_validate(model, data, cv=cv)
        tmp = pd.DataFrame(cv_results).mean()
        tmp['model'] = model_name
        results = results.append(tmp, ignore_index=True)

    return results

def generate_models_dict(models, sim_names, user_based):
    models_dict = {}

    for sim_name in sim_names:
        sim_dict = {
            'name': sim_name,
            'user_based': user_based
        }
        for model in models:
            model_name = get_model_name(model) + ' ' + sim_name
            models_dict[model_name] = model(sim_options=sim_dict)

    return models_dict

df = pd.read_csv(Path('book-review-dataset/top_ratings.csv'))

reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(df[['user_id', 'isbn', 'book_rating']], reader)

print('Number of ratings: %d\nNumber of books: %d\nNumber of users: %d' % (len(df), len(df['isbn'].unique()), len(df['user_id'].unique())))

models1 = generate_models_dict([KNNBasic, KNNWithMeans, KNNWithZScore, KNNBaseline], ['pearson'], True)
results1 = cv_multiple_models(data, models1)
models1 = None
print(results1)


models2 = generate_models_dict([KNNBaseline], ['cosine', 'msd', 'pearson'], True)
results2 = cv_multiple_models(data, models2)
models2 = None
print(results2)
