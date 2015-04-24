import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
from utilities.plotBucket import plotBucket
from utilities.plotBucket import plotBar

df_rating = pd.read_pickle(
    "savedFrames/ratingPrediction/ratingTable")
df_paper = pd.read_pickle(
    "savedFrames/summaryStatistics/papersTable")

p1 = plotBucket(
    df_rating,
    "authorsMaxPastPaper",
    "rating",
    color="blue",
    x_label="Number of Past Papers",
    y_label="Average Rating")
setp(p1, linewidth=1.5)

p2 = plotBucket(
    df_rating,
    "primaryAuthorPastPaperCount",
    "rating",
    color="red",
    sameFigure=True,
    marker="s")
setp(p2, linewidth=1.5)
legend([p1, p2], ["Most Experienced Author", "Primary Author"], loc=4)


p1 = plotBucket(
    df_paper,
    "authorsMaxPastPaper",
    "accepted",
    delta=10,
    color="blue",
    x_label="Number of Past Papers",
    y_label="P(Accept)")
setp(p1, linewidth=1.5)

p2 = plotBucket(
    df_paper,
    "primaryAuthorPastPaperCount",
    "accepted",
    delta=10,
    color="red",
    sameFigure=True,
    marker="s")
setp(p2, linewidth=1.5)
legend([p1, p2], ["Most Experienced Author", "Primary Author"], loc=4)

show()