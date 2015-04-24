import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
from utilities.plotBucket import plotBar
from utilities.plotBucket import plotBucket

acceptanceRate = 152.0/998.0

papersFrame = pd.read_pickle(
    "savedFrames/summaryStatistics/papersTable")
userFrame = pd.read_pickle(
    "savedFrames/summaryStatistics/userTable")



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

authorFrame = userFrame[userFrame["#Papers"] > 0]
authorFrame["acceptanceRate"] = authorFrame["#Accepted"] \
    * 1.0/authorFrame["#Papers"]
plotBar(
    authorFrame,
    "#Papers",
    "acceptanceRate",
    [0, 1, 2, 3, 4, 5],
    title="Acceptance Rate vs. Number of Submissions",
    x_label="Number of Submissions",
    y_label="Acceptance Rate",
    xlim=[0, 6]
)


plotBucket(
    userFrame,
    "#PastPapers",
    "#Papers",
    x_label="Number of Past Papers",
    y_label="Number of Submissions",
    x_percentile=False,
    xlim=[0, 200])


plotBucket(
    authorFrame,
    "#PastPapers",
    "acceptanceRate",
    x_label="Number of Past Papers",
    y_label="Acceptance Rate",
    x_percentile=False,
    color="Red",
    xlim=[0, 200])

plotBucket(
    papersFrame,
    "authorsMaxPastPaper",
    "accepted",
    x_label="Max Number of Past Papers of Authors",
    y_label="P(Accept)",
    x_percentile=False,
    color="Green",
    xlim=[0, 200])

show()