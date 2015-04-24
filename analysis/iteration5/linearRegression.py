import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
    import numpy as np
from sklearn.linear_model import LinearRegression, Lasso, ElasticNet
from sklearn.svm import LinearSVC
from sklearn import cross_validation
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
import random
import math

df = pd.read_pickle(
    "savedFrames/predictionFeatures/paperTable")

##Perform's Cross Validation
##Arguments: dataframe, model to train
def performCV(df, y_name, accept, model, preProcess):
    n = 10
    k = 10
    sumOfMeans = 0
    for i in range(n):
        rows_r = range(df.shape[0])
        random.shuffle(rows_r)
        df = df.iloc[rows_r].reset_index(drop=True)
        df_target = df[y_name]
        df_accept = df[accept]
        df_train = df.drop([y_name, accept], 1)

        X = preProcess(df_train)
        kf = cross_validation.KFold(X.shape[0], k)
        totalCorrect = 0
        for train, test in kf:
            model.fit(X.ix[train], df_target.ix[train])
            pRatings = model.predict(X.ix[test])
            pAccept = pRatings > -0.03
            print pAccept.sum()
            correct = (1 - pAccept - df_accept.ix[test].values).sum()
            totalCorrect += correct
        sumOfMeans += totalCorrect * 1.0/df.shape[0]
    print "Mean: %f" % (sumOfMeans/n)


    #     sumOfMeans += scores.mean()
    #     sumOfSTD += scores.std()

    # mean_cv = sumOfMeans/n
    # std_cv = (sumOfSTD/n)/math.sqrt(n)

    # print "y: %s, Mean: %f, Stddev: %f" % (y_name, mean_cv, std_cv)

    # return mean_cv, std_cv


##Calculates Baseline using a variety of characteristics
def calcBaseline(df):
    numAccepted = 0.0
    correctAccepted = 0.0
    numRejected = 0.0
    correctRejected = 0.0

    for i in range(df.shape[0]):
        accept = False
        row = df.iloc[i]

        #if row["modeAuthorCountry"] == "Germany":
        #    accept = True

        # if row["maxTopPaperCount"] > 300:
        #     accept = True

        # if row["maxKDDPaperCount"] > 5:
        #     accept = True

        if row["accepted"]:
            numAccepted += 1
            correctAccepted += accept
        else:
            numRejected += 1
            correctRejected += not accept

    print "Baseline accept: %f" % (
        1.0*(correctAccepted + correctRejected)/(numAccepted + numRejected))

def preProcess(X):
    # X = normalize(X, axis=0, copy=False)

    # pca = PCA(n_components = 4)
    # X = pca.fit_transform(X)
    return X

features = [
    # "modeAuthorCountry",
    # "maxAuthorCountry",
    # "primaryAuthorCountry",
    # "affiliation",
    # "avgPaperCount",
    # "maxPaperCount",
    # "primaryPaperCount",
    # "avgTopPaperCount",
    # "maxTopPaperCount",
    # "primaryTopPaperCount",
    # "avgKDDPaperCount",
    # "maxKDDPaperCount",
    # "primaryKDDPaperCount",
    # "maxConnectivity",
    # "maxPageRank",
    # "maxDegCentrality",
    # "numAuthors",
    # "avgPaperCountLog",
    "maxPaperCountLog",
    # "primaryPaperCountLog",
    # "avgTopPaperCountLog",
    "maxTopPaperCountLog",
    # "primaryTopPaperCountLog",
    # "avgKDDPaperCountLog",
    "maxKDDPaperCountLog",
    # "primaryKDDPaperCountLog",
    "maxConnectivityLog",
    # "maxPageRankLog",
    "maxDegCentralityLog",
    "numAuthorsLog",
    # "avgLogPaperCount",
    # "avgLogTopPaperCount"
]

featuresAccept = features + ["avgRating", "accepted"]
performCV(df[featuresAccept], "avgRating", "accepted", Lasso(alpha=0.1), preProcess)
calcBaseline(df)
