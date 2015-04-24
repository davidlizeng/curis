import cPickle
from feature_extraction.dataLoader import DataLoader
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn.decomposition import PCA
from sklearn.lda import LDA
from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler
import numpy as np
import random
import math


print "Loading Files"


def readFile(name):
    f = open("savedFrames/iteration5/reviewPrediction/"+name, 'r')
    obj = cPickle.load(f)
    f.close()
    return obj

#types = ["Text"]
types = ["Comment", "Strength", "Weakness"]


termDict = readFile("termDict.dat")
paperIds = readFile("paperIds.dat")
paperMatrices = [readFile("paper" + t + "Matrix.mat") for t in types]
reviewInfo = readFile("reviewInfo.dat")
reviewMatrices = [readFile("review" + t + "Matrix.mat") for t in types]

print "Load Data"

loader = DataLoader()
loader.loadUsers()
loader.loadPapers()
loader.loadReviews()
loader.loadAcceptance()


def performCV(X, y, model, n=4):
    predictions = np.zeros(X.shape[0])

    X = np.array(X)
    X = X.T[~np.all(X == 0, axis=0)].T
    X = normalize(X, axis=1, norm='l2')
    # X = StandardScaler().fit_transform(X)
    pca = PCA(n_components = X.shape[0]/30)
    X = pca.fit_transform(X)
    rejectedIndices = [
        i
        for i, yi in enumerate(y)
        if yi == 0
    ]

    acceptedIndices = [
        i
        for i, yi in enumerate(y)
        if yi == 1
    ]

    numSamples = len(acceptedIndices)

    sumOfMeansCV = 0.0
    sumOfSTDCV = 0.0
    sumOfMeansTrain = 0.0

    for iteration in range(n):
        print iteration
        random.shuffle(rejectedIndices)
        rejectedSample = rejectedIndices[:numSamples]

        allIndices = np.array(rejectedSample + acceptedIndices)

        Xtrain = X[allIndices]
        ytrain = np.array(y)[allIndices]

        print Xtrain.shape

        scores = cross_validation.cross_val_score(
            model, Xtrain, ytrain, cv=10)

        sumOfMeansCV += scores.mean()
        sumOfSTDCV += scores.std()

        sumOfMeansTrain += model.fit(Xtrain, ytrain).score(Xtrain, ytrain)
        predictions += model.predict(X)

    mean_cv = sumOfMeansCV/n
    std_cv = (sumOfSTDCV/n)/math.sqrt(n)
    accuracy = abs(np.ones(len(y)) - y - (predictions / n))

    print "Training Mean: %f" % (sumOfMeansTrain/n)
    print "CV Mean: %f, Stddev: %f" % (mean_cv, std_cv)

    return accuracy

y = [
    1 if loader.papers[id].accepted else 0
    for id in paperIds
]

fields = ["presentation", ]
otherPaperRatings = np.empty([len(y), len(fields)])
count = 0
for id in paperIds:
    p = loader.papers[id]
    if len(p.reviews) == 0:
        otherRatings[count] = np.zeros([1, len(fields)])
    else:
        num = len(p.reviews) * 1.0
        otherPaperRatings[count] = \
            [sum([r.ratings[f] for r in p.reviews])/num for f in fields]
    count += 1

paperMatrix = np.concatenate([p.todense() for p in paperMatrices], axis=1)
#paperMatrix = np.concatenate((paperMatrix, otherPaperRatings), axis=1)
#paperMatrix = otherPaperRatings
accuracy = performCV(paperMatrix, y, SVC(C=0.5, kernel='linear'), n=100)
# f = open('analysis/iteration5/reviewAccuracyByPaper.csv', 'wb')
# for id, acc in zip(paperIds, accuracy):
#     f.write("%d,%f\n" % (id, acc))



# y = [
#     1 if loader.reviews[id].paper.accepted else 0
#     for id in reviewInfo
# ]

# accuracy = performCV(reviewMatrix.todense(), y, SVC(C=1, gamma=1), n=25)
# f = open('analysis/iteration5/reviewAccuracyByReview.csv', 'wb')
# for id, acc in zip(reviewInfo, accuracy):
#     f.write("%d,%f\n" % (id, acc))


y = [
    1 if loader.reviews[id].overallRating > 0 else 0
    for id in reviewInfo
]
otherReviewRatings = np.empty([len(y), len(fields)])
count = 0
for id in reviewInfo:
    r = loader.reviews[id]
    otherReviewRatings[count] = \
        [r.ratings[f] for f in fields]
    count += 1
reviewMatrix = np.concatenate([r.todense() for r in reviewMatrices], axis=1)
#reviewMatrix = np.concatenate((reviewMatrix, otherReviewRatings), axis=1)
#reviewMatrix = otherReviewRatings
accuracy = performCV(reviewMatrix, y, SVC(C=1, kernel='linear'), n=25)
# f = open('analysis/iteration5/reviewAccuracyRating.csv', 'wb')
# for id, acc in zip(reviewInfo, accuracy):
#     f.write("%d,%f\n" % (id, acc))

