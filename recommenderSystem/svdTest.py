import itertools
from collections import defaultdict

from BookData import BookData
from surprise import SVD, accuracy
from surprise.model_selection import train_test_split


class SVDEvaluator:
    def MAE(predictions):
        return accuracy.mae(predictions, verbose=False)

    def RMSE(predictions):
        return accuracy.rmse(predictions, verbose=False)


bd = BookData()

print("Loading movie ratings...")
data = bd.loadBookData()

print("\nBuilding recommendation model...")
trainSet, testSet = train_test_split(data, test_size=0.20, random_state=1)

algo = SVD(random_state=10)
algo.fit(trainSet)

print("\nComputing recommendations...")
predictions = algo.test(testSet)

print("\nEvaluating accuracy of model...")
print("RMSE: ", SVDEvaluator.RMSE(predictions))
print("MAE: ", SVDEvaluator.MAE(predictions))
