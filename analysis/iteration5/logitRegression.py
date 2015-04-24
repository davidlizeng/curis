import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
    import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.decomposition import PCA
from sklearn import cross_validation
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import random
import cPickle
from feature_extraction.dataLoader import DataLoader
import math
from sets import Set

###SETTINGS
useAbstract = False
withPredictions = False
useBootstrap = True
useExtreme = False


###LOAD IN DATA
def readFile(name):
    f = open("savedFrames/iteration5/abstractPrediction/"+name, 'r')
    obj = cPickle.load(f)
    f.close()
    return obj

if useAbstract:
    termDict = readFile("termDict.dat")
    paperIds = readFile("paperIds.dat")
    paperMatrix = readFile("paperMatrix.mat")

loader = DataLoader()
loader.loadPapers()
loader.loadAcceptance()

df_paper = pd.read_pickle(
    "savedFrames/predictionFeatures/paperTable")
df = df_paper


###HELPER FUNCTIONS FOR CLASSFIER
def randomSample(n, k):
    return [
        int(random.random() * n)
        for i in range(k)
    ]


##Performs Cross Validation
##Arguments: dataframe, model to train
def performCV(df, model, n=50):

    #Get Data
    y = df["accepted"].values
    X = df.drop(["accepted", "avgRating"], 1).values

    X = preProcess(X)

    #Predictions vector for assessing accuracy
    if withPredictions:
        predictions = np.zeros(X.shape[0])

    #Indices in data set of accepted and rejected values
    rejectedIndices = np.array([
        i
        for i, yi in enumerate(y)
        if yi == 0
    ])

    rejectedSet = Set(rejectedIndices)

    acceptedIndices = np.array([
        i
        for i, yi in enumerate(y)
        if yi == 1
    ])
    if useExtreme:
        yrat = df["avgRating"].values

        y = np.array([0 if abs(r) < 1 else 1 if a else 2 for a, r in zip(y, yrat)])

    if useBootstrap:
        acceptedSet = Set(acceptedIndices)
        samples = int(2*len(acceptedIndices))

    else:
        #num samples is 2/3 of the accepted data
        samples = len(acceptedIndices)
        numTrainSamples = samples - int(samples/3.0)

    #For keeping track of performance
    acceptedTestScores = []
    rejectedTestScores = []
    testScores = []
    trainScores = []

    #MAIN LOOP
    for iteration in range(n):

        if useBootstrap:

            acceptedTrain =\
                acceptedIndices[randomSample(len(acceptedIndices), samples)]
            rejectedTrain =\
                rejectedIndices[randomSample(len(rejectedIndices), samples)]

            acceptedTest = list(acceptedSet.difference(Set(acceptedTrain)))
            rejectedTest = list(rejectedSet.difference(Set(rejectedTrain)))

        else:
            #Get Samples and Partition into Train and Test
            def partitionData(indices):
                random.shuffle(indices)

                return\
                    indices[:numTrainSamples], indices[numTrainSamples:samples]

            acceptedTrain, acceptedTest = partitionData(acceptedIndices)
            rejectedTrain, rejectedTest = partitionData(rejectedIndices)

        train = np.concatenate((acceptedTrain, rejectedTrain))

        #Train Model
        model.fit(X[train], y[train])

        #Score Model
        trainScores.append(model.score(X[train], y[train]))

        acceptedScore = model.score(X[acceptedTest], y[acceptedTest])
        rejectedScore = model.score(X[rejectedTest], y[rejectedTest])

        #Record Scores
        acceptedTestScores.append(acceptedScore)
        rejectedTestScores.append(rejectedScore)
        testScores.append(.5*(acceptedScore + rejectedScore))

        #Record Predictions
        if withPredictions:
            predictions += model.predict(X)

    print "\n"
    print "         Training Score:  %.3f  +/- %.4f" % (
        np.mean(trainScores),
        np.std(trainScores)*1.0/math.sqrt(n))
    print "             Test Score:  %.3f  +/- %.4f" % (
        np.mean(testScores),
        np.std(testScores)*1.0/math.sqrt(n))
    print "  Test Score (Accepted):  %.3f  +/- %.4f" % (
        np.mean(acceptedTestScores),
        np.std(acceptedTestScores)*1.0/math.sqrt(n))
    print "  Test Score (Rejected):  %.3f  +/- %.4f" % (
        np.mean(rejectedTestScores),
        np.std(rejectedTestScores)*1.0/math.sqrt(n))

    if withPredictions:
        accuracy = abs(np.ones(len(y)) - y - (predictions / n))

        return accuracy

    return np.mean(testScores)


##Calculates Baseline using a variety of characteristics
def calcBaseline(df):
    numAccepted = 0.0
    correctAccepted = 0.0
    numRejected = 0.0
    correctRejected = 0.0

    for i in range(df.shape[0]):
        accept = False
        row = df.iloc[i]

        # if row["modeAuthorCountry"] == "Germany":
        #     accept = True

        if row["maxTopPaperCount"] > 18:
            accept = True

        if row["maxKDDPaperCount"] > 3:
            accept = True

        if row["accepted"]:
            numAccepted += 1
            correctAccepted += accept
        else:
            numRejected += 1
            correctRejected += not accept

    # print "Baseline reject: %f" % (
    #     1.0 * (correctAccepted + correctRejected)
    #     / (numAccepted + numRejected))
    #print correctAccepted, correctRejected
    #print numAccepted, numRejected
    print "Baseline simple: %f" % (
        correctAccepted * 0.5 / numAccepted +
        correctRejected * 0.5 / numRejected)


def preProcess(X):
    X = StandardScaler().fit_transform(X)
    # pca = PCA(n_components=5)
    # X = pca.fit_transform(X)
    # print pca.n_components
    return X

features = [
    # "accepted",
    # "modeAuthorCountry",
    # "maxAuthorCountry",
    # "primaryAuthorCountry",
#    "isIndustry",
#    "isAcademic",
#    "isMixed",
    # "avgPaperCount",
    # "maxPaperCount",
    # "primaryPaperCount",
    # "avgTopPaperCount",
    # "maxTopPaperCount",
    # "primaryTopPaperCount",
#    "avgKDDPaperCount",
#    "maxKDDPaperCount",
#    "primaryKDDPaperCount",
    "maxConnectivity",
    "maxPageRank",
    "maxDegCentrality",
#    "numAuthors",
   #  "avgPaperCountLog",
   #  "maxPaperCountLog",
   #  "primaryPaperCountLog",
   #  "avgTopPaperCountLog",
   #  "maxTopPaperCountLog",
   #  "primaryTopPaperCountLog",
   # "avgKDDPaperCountLog",
   # "maxKDDPaperCountLog",
   # "primaryKDDPaperCountLog",
    "maxConnectivityLog",
    "maxPageRankLog",
    "maxDegCentralityLog",
    # "numNoDBLP",
    # "numCC",
    # "density",
    # "avgCCSize",
    # "maxCCSize",
#    "numAuthorsLog",
    # "avgLogPaperCount",
    # "avgLogTopPaperCount",
    # "revPaperCount",
    # "revTopPaperCount",
    # "revKDDPaperCount",
    # "maxSimilarity",
    # "primarySimilarity",
    # "maxJacSimilarity",
    # "primaryJacSimilarity",
    # "minDist",
    # "avgDist",
    # "revPaperCountLog",
    # "revTopPaperCountLog",
    # "revKDDPaperCountLog",
    "minDist",
    "avgMinDist",
    "minAvgDist",
    "avgDist",
    "avgSimilarity",
    "maxSimilarity",
    "avgMaxSimilarity",
]

base = [
    "accepted",
    "avgRating",
]

authorPastPaper = [
    "maxTopPaperCount",
    "avgPaperCountLog",
    "avgTopPaperCountLog",
    "primaryKDDPaperCountLog",
]

authorConnectivity = [
    "maxConnectivity",
    "maxDegCentrality",
    "maxConnectivityLog",
]

reviewer = [
    "avgMinDist",
    "avgMaxSimilarity"
]

structure = [
    "numNoDBLP",
    # "numCC",
    "density",
    "avgCCSize",
    "numConn",
    # "maxCCSize",
]


#SET THE CORRECT FEATURE SET HERE
featureSet = base + authorConnectivity + authorPastPaper + structure

if useAbstract:
    X = paperMatrix.todense()
    X = np.array(X)
    X = X.T[~np.all(X == 0, axis=0)].T
    X = normalize(X, axis=1, norm='l2')
    X = PCA(100).fit_transform(X)
    df_abstracts = pd.DataFrame(X)
    df_abstracts["paperId"] = np.array(paperIds)

    df_X = pd.merge(df[featureSet + ["paperId"]], df_abstracts, on="paperId")
    df_X = df_X.drop("paperId", axis=1)
else:
    df_X = df[featureSet]

#default setting C = .5
#settinc C = .05 when using all
model = SVC(C=.5)
performCV(df_X, model, 50)


# #FOR FEATURE SELECTION
# d = {}
# for i in features:
#     if i not in mySet:
#         print i
#         d[i] = performCV(df[mySet + [i]], SVC(C=.5), 20)
# for i, d in d.iteritems():
#     print "%s: %f" % (i, d)

"""
##HEATMAP CODE
m = 100
n = 100
col1 = "avgTopPaperCountLog"
col2 = "maxPageRank"

predictions = np.zeros((m, n))
xs = list(np.linspace(df[col1].min(), df[col1].max(), m+1))
ys = list(np.linspace(df[col2].min(), df[col2].max(), n+1))

for i in range(m):
    for j in range(n):

        predictions[i][j] = model.predict([xs[i], ys[j]])

figure(facecolor="White")
imshow(predictions, cmap="Blues")

xlabel("Most Experienced Author Paper Count")
ylabel("Primary Author Paper Count")
suptitle("Heatmap of P(Accept)")
colorbar()

#show()
"""
