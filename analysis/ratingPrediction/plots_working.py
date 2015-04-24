import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
    import numpy as np
from utilities.plotBucket import plotBucket
from utilities.plotBucket import plotBar
from utilities.plotBucket import plotFrequencyHistogram
import math


df_rating = pd.read_pickle(
    "savedFrames/ratingPrediction/ratingTable")
df_paper = pd.read_pickle(
    "savedFrames/summaryStatistics/papersTable")
df_reviewer = pd.read_pickle(
    "savedFrames/summaryStatistics/reviewerTable")
df_dist = pd.read_pickle(
    "savedFrames/reviewStatistics/reviewTable")
userFrame = pd.read_pickle(
    "savedFrames/summaryStatistics/userTable")
papersFrame = pd.read_pickle(
    "savedFrames/summaryStatistics/papersTable")
df_mostSimilar = pd.read_pickle(
    "savedFrames/ratingPrediction/mostSimilarTable")

df = pd.merge(df_rating, df_dist, on=['paperId', 'userId', 'rating'])
df = pd.merge(df, df_mostSimilar, on=['paperId'])
df = pd.merge(df,
              papersFrame[["paperId",
                           "maxConnectivity",
                           "primarySpecificSubjectArea",
                           "primarySubjectArea"]],
              on=["paperId"])

##columns of interest
#paperId

maxSimCol = "maxAuthorReviewerSimilarity"


def plotTest(df, col, col2):
    plotBucket(
        df,
        col,
        col2)

p = plotBucket(
    df,
    maxSimCol,
    "rating",
    x_label="Similarity",
    y_label="Rating",
    delta=15,
    title=
    "Average Rating vs. Similarity of Reviewer to Most Experienced Author",
    marker="s",
    color="green",
    xlim=[0, 100]
)
setp(p, linewidth=2, alpha=1)

p = plotBucket(
    df,
    "authorReviewerSimilarity",
    "rating",
    x_label="Similarity",
    y_label="Rating",
    delta=15,
    title=
    "Average Rating vs. Similarity of Reviewer to Most Experienced Author",
    marker="s",
    color="red",
    sameFigure=True,
    xlim=[0, 100]
)
setp(p, linewidth=2, alpha=1)

dfconn = df[df["maxConnectivity"] > 0]
xs = np.log(dfconn["maxConnectivity"].values)
A = array([xs, ones(len(xs))])
ys = dfconn[maxSimCol].values

w = np.linalg.lstsq(A.T, ys)[0]

x = np.logspace(1, 5, 100)
yfit = w[0]*np.log(x) + w[1]

plotBucket(
    dfconn,
    "maxConnectivity",
    maxSimCol,
    x_label="Connectivity of Most Connected Author",
    y_label="Similarity between Author and Reviewer",
    title="Similarity vs. Connectivity",
    delta=5,
    x_percentile=False,
    plotMean=False,
    xlim=[50, 100000]
)
gca().set_xscale('log')
plt.plot(x, yfit, 'k--')


# def plotBucket(
#         df,
#         xcol,
#         ycol,
#         delta=5,
#         color="blue",
#         title="default",
#         x_label="default",
#         y_label="default",
#         x_percentile=True,
#         xlim=None):

show()