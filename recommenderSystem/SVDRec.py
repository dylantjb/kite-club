from BookData import BookData
from surprise import SVD


def BuildAntiTestSetForUser(testSubject, trainset):
    fill = trainset.global_mean

    anti_testset = []
    
    u = trainset.to_inner_uid(str(testSubject))
    
    user_items = set([j for (j, _) in trainset.ur[u]])
    anti_testset += [(trainset.to_raw_uid(u), trainset.to_raw_iid(i), fill) for
                             i in trainset.all_items() if
                             i not in user_items]
    return anti_testset

# Pick an arbitrary test subject
testSubject = 276747

bd = BookData()

print("Loading book ratings...")
data = bd.loadBookData()

userRatings = bd.getUserRatings(testSubject)
loved = []
hated = []
for ratings in userRatings:
    if (float(ratings[1]) > 4.0):
        loved.append(ratings)
    if (float(ratings[1]) < 3.0):
        hated.append(ratings)

print("\nUser ", testSubject, " loved these books:")
for ratings in loved:
    print(bd.getBookName(ratings[0]))

print("\nBuilding recommendation model...")
trainSet = data.build_full_trainset()

algo = SVD()
algo.fit(trainSet)

print("Computing recommendations...")
testSet = BuildAntiTestSetForUser(testSubject, trainSet)
predictions = algo.test(testSet)

recommendations = []

print ("\nWe recommend:")
for userID, bookID, actualRating, estimatedRating, _ in predictions:
    intBookID = bookID
    recommendations.append((intBookID, estimatedRating))

recommendations.sort(key=lambda x: x[1], reverse=True)

for ratings in recommendations[:10]:
    print(bd.getBookName(ratings[0]))