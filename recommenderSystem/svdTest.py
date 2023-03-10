from BookData import BookData
from surprise import SVD
from surprise.model_selection import train_test_split

import itertools

from surprise import accuracy
from collections import defaultdict

class SVDEvaluator:

    def MAE(predictions):
        return accuracy.mae(predictions, verbose=False)

    def RMSE(predictions):
        return accuracy.rmse(predictions, verbose=False)

bd = BookData()

print("Loading movie ratings...")
data = bd.loadBookData()

print("\nBuilding recommendation model...")
trainSet, testSet = train_test_split(data, test_size=.20, random_state=1)

algo = SVD(random_state=10)
algo.fit(trainSet)

print("\nComputing recommendations...")
predictions = algo.test(testSet)

print("\nEvaluating accuracy of model...")
print("RMSE: ", SVDEvaluator.RMSE(predictions))
print("MAE: ", SVDEvaluator.MAE(predictions))