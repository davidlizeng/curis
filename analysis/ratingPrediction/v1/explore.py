import warnings
import random as rndm
from pylab import *
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error
from scipy import stats
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from pandas import DataFrame, Series
    from pandas.tools.plotting import scatter_matrix
    import pandas as pd


def addNoise(series, stddev):
    return series + stddev*np.random.randn(len(series))


def plotscatter(col, df):
    plt.scatter(addNoise(df[col], .2), addNoise(df["rating"], .2), alpha=.2)

acceptanceRate = 152.0/998.0

ratingsFrame = pd.read_pickle(
    "savedFrames/ratingPrediction/ratingTable")

# columns = [
#     "#Authors",
#     "#Bids",
#     "abstractWordCount",
#     "authorsMaxPastPaper",
#     "authorsPastPaperCount",
#     "titleWordCount",
# ]

# columnsWith = columns + ["accepted"]

# df = papersFrame[columnsWith].dropna()
# data = preprocessing.scale(df[columns].values.astype(float32))
# target = df["accepted"].values.astype(int32)

#scatter_matrix(ratingsFrame, alpha=0.2, figsize=(50, 50), diagonal='kde')
plt.figure(2)
plotscatter("specificCommonSubjects", ratingsFrame)
plt.figure(3)
plotscatter("generalCommonSubjects", ratingsFrame)
plt.figure(4)
plotscatter("samePrimaryGeneralSubject", ratingsFrame)
plt.figure(5)
plotscatter("samePrimarySpecificSubject", ratingsFrame)
plt.figure(6)
plotscatter("pastPaperSimilarity", ratingsFrame)
plt.figure(7)
plotscatter("authorReviewerSimilarity", ratingsFrame)

# clf = svm.SVC(kernel='linear', C=10)
# scores = cross_validation.cross_val_score(
#     clf, data, target, cv=10)
# print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

enet = ElasticNet(alpha=.1, l1_ratio=.7)
df = ratingsFrame.drop('rating', axis = 1)

nrows = df.shape[0]
split = int(.9 * nrows)

rows = range(nrows)
rndm.shuffle(rows)

train_index = df.index[rows[:split]]
test_index = df.index[rows[split:]]

xtrain = df.ix[train_index, :]
ytrain = ratingsFrame["rating"][train_index]
xtest = df.ix[test_index, :]
ytest = ratingsFrame["rating"][test_index]


y_pred = enet.fit(xtrain, ytrain).predict(xtest)
error = mean_squared_error(ytest, y_pred)
print("Predict Model")
print(error)
print(enet.coef_)

ypredmean = (y_pred*0) + ratingsFrame["rating"].mean()
print("Predict Mean")
print(mean_squared_error(ytest, ypredmean))

print("Predict Zero")
y_pred0 = y_pred * 0
print(mean_squared_error(ytest, y_pred0))


def runTTest(col, df):
    print "t-Test for %s" % col
    d1 = df[df[col] == True]["rating"]
    d2 = df[df[col] != True]["rating"]
    print "Number of Samples: (%d, %d)" % (d1.shape[0], d2.shape[0])
    print "Means: (%f, %f)" %(d1.mean(), d2.mean())
    print stats.ttest_ind(d1, d2)

runTTest("samePrimarySpecificSubject", ratingsFrame)
runTTest("samePrimaryGeneralSubject", ratingsFrame)

ratingsFrame["pastPaperSimilar"] = (
    ratingsFrame["pastPaperSimilarity"] >
    ratingsFrame["pastPaperSimilarity"].mean()
)
runTTest("pastPaperSimilar", ratingsFrame)

ratingsFrame["authorReviewerSimilar"] = (
    ratingsFrame["authorReviewerSimilarity"] >
    ratingsFrame["authorReviewerSimilarity"].mean()
)
runTTest("authorReviewerSimilar", ratingsFrame)


myHist, bins = np.histogram(ratingsFrame["authorReviewerSimilarity"],
   [0,.01,.02,.03,.04,.05,.06,.07,.08,.09,.1,.11,.12,.13,.14,.15,.16,.17,.18,.19,.2])
width = (bins[1] - bins[0])*.95
center = (bins[:-1] + bins[1:])/2
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)
fig.set_facecolor("white")
ax.bar(center, myHist, align='center', width=width)



show()

