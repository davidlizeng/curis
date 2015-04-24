import cPickle
from feature_extraction.dataLoader import DataLoader
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn.preprocessing import normalize
import numpy as np
import random
import math
import random
from sklearn.decomposition import PCA

print "Loading Files"


def readFile(name):
    f = open("savedFrames/iteration5/abstractPrediction/"+name, 'r')
    obj = cPickle.load(f)
    f.close()
    return obj

termDict = readFile("termDict.dat")
paperIds = readFile("paperIds.dat")
paperMatrix = readFile("paperMatrix.mat")

print "Load Data"

loader = DataLoader()
loader.loadPapers()
loader.loadAcceptance()


def randomSample(n, k):
    return [
        int(random.random() * n)
        for i in range(k)
    ]


def performCV(X, y, model, n=4):
    predictions = np.zeros(X.shape[0])

    X = np.array(X)
    y = np.array(y)
    X = X.T[~np.all(X == 0, axis=0)].T
    X = normalize(X, axis=1, norm='l2')
    X = PCA(100).fit_transform(X)

    rejectedIndices = np.array([
        i
        for i, yi in enumerate(y)
        if yi == 0
    ])

    acceptedIndices = np.array([
        i
        for i, yi in enumerate(y)
        if yi == 1
    ])

    numSamples = int(len(acceptedIndices) * 2)

    acceptedTestScores = []
    rejectedTestScores = []
    trainScores = []

    for iteration in range(n):
        rejectedSample =\
            rejectedIndices[randomSample(len(rejectedIndices), numSamples)]
        acceptedSample =\
            acceptedIndices[randomSample(len(acceptedIndices), numSamples)]

        allIndices = np.concatenate((rejectedSample, acceptedSample))

        Xtrain = X[allIndices]
        ytrain = y[allIndices]

        #print Xtrain.shape
        acceptedSample.sort()
        acceptedComplement = []
        j = 0
        for i in range(len(acceptedIndices)):
            while j < len(acceptedSample)\
                    and acceptedSample[j] < acceptedIndices[i]:
                j += 1
            if j == len(acceptedSample)\
                    or acceptedSample[j] != acceptedIndices[i]:
                acceptedComplement.append(acceptedIndices[i])

        rejectedSample.sort()
        rejectedComplement = []
        j = 0
        for i in range(len(rejectedIndices)):
            while j < len(rejectedSample)\
                    and rejectedSample[j] < rejectedIndices[i]:
                j += 1
            if j == len(rejectedSample)\
                    or rejectedSample[j] != rejectedIndices[i]:
                rejectedComplement.append(rejectedIndices[i])

        model.fit(Xtrain, ytrain)

        acceptedTestScores.append(
            model.score(X[acceptedComplement], y[acceptedComplement]))
        rejectedTestScores.append(
            model.score(X[rejectedComplement], y[rejectedComplement]))
        trainScores.append(model.score(Xtrain, ytrain))

        predictions += model.predict(X)

        if iteration % 25 == 0 and iteration > 0:
            print iteration

    print "Training Scores -- Mean: %.2f, Stddev: %.4f" % (
        np.mean(trainScores), np.std(trainScores))
    print "Accepted Test Scores -- Mean: %.2f, Stddev: %.4f" % (
        np.mean(acceptedTestScores), np.std(acceptedTestScores))
    print "Rejected Test Scores -- Mean: %.2f, Stddev: %.4f" % (
        np.mean(rejectedTestScores), np.std(rejectedTestScores))

    accuracy = abs(np.ones(len(y)) - y - (predictions / n))

    return accuracy

y = [
    1 if loader.papers[id].accepted else 0
    for id in paperIds
]

# for c in [.01, .1, .5, 1]:
#     print c
#     accuracy = performCV(paperMatrix.todense(), y, SVC(C=c, kernel='linear'), n=50)

accuracy = performCV(paperMatrix.todense(), y, SVC(C=.5, kernel='linear'), n=100)

f = open('analysis/iteration5/abstractAccuracyByPaper_PCA.csv', 'wb')
for id, acc in zip(paperIds, accuracy):
    f.write("%d,%f\n" % (id, acc))
