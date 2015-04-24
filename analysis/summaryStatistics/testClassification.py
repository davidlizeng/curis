import warnings
import matplotlib as mpl
from pylab import *
from sklearn import svm
from sklearn import cross_validation
from sklearn import preprocessing
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from pandas import DataFrame, Series
    from pandas.tools.plotting import scatter_matrix
    import pandas as pd


acceptanceRate = 152.0/998.0

papersFrame = pd.read_pickle(
    "savedFrames/summaryStatistics/papersTable")

columns = [
    "#Authors",
    "#Bids",
    "abstractWordCount",
    "authorsMaxPastPaper",
    "authorsPastPaperCount",
    "titleWordCount",
]

columnsWith = columns + ["accepted"]

df = papersFrame[columnsWith].dropna()
data = preprocessing.scale(df[columns].values.astype(float32))
target = df["accepted"].values.astype(int32)

scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')

clf = svm.SVC(kernel='linear', C=10)
scores = cross_validation.cross_val_score(
    clf, data, target, cv=10)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

show()
