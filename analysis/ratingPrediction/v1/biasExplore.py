import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
from utilities.plotBucket import plotBucket
from utilities.plotBucket import plotBar


df = pd.read_pickle(
    "savedFrames/ratingPrediction/ratingTable")
dfOther = pd.read_pickle(
    "savedFrames/reviewStatistics/reviewTable")

dfx = df

df_original = pd.merge(df, dfOther, on=['paperId', 'userId', 'rating'])


#BIAS EXPLORATION
columns = [
    "paperId",
    "userId",
    "rating",
    "authorReviewerSimilarity",
    "pastPaperSimilarity",
    "maxAuthorReviewerSimilarity",
    "minDist",
]

df = df_original[columns]
df2 = df.copy()
df2.columns = [
    "paperId",
    "userId2",
    "rating2",
    "authorReviewerSimilarity2",
    "pastPaperSimilarity2",
    "maxAuthorReviewerSimilarity2",
    "minDist2"
]

df = pd.merge(df, df2, on='paperId')

df = df[(df["userId"] != df["userId2"]) & (df["rating"] != df["rating2"])]

df["simDiff"] = df["authorReviewerSimilarity"] - df["authorReviewerSimilarity2"]
df["distDiff"] = df["minDist"] - df["minDist2"]
df["higherRating"] = df["rating"] > df["rating2"]

plotBucket(
    df,
    "simDiff",
    "higherRating",
    x_label="Difference in Author/Reviewer Similarity",
    y_label="Probability of a Higher Rating",
    delta=10,
    x_percentile=False,
    xlim=[-.1, .1])

df_dist = df[df["distDiff"] >= 0]
plotBucket(
    df,
    "distDiff",
    "higherRating",
    delta=5,
    x_label="Difference in Min Distance to Reviewer",
    y_label="Probability of a Higher Rating",
    color="Green",
    x_percentile=False)

plotBar(
    df_original,
    "minDist",
    "paperRatingDiff",
    [1, 2, 3, 4, 5, 6, 7, 8],
    x_label="Min Distance between Reviewer and Paper Authors",
    y_label="Deviation from Paper Average Rating",
    title="Deviation from Paper Average vs. Min Dist to Reviewer",
    color="Blue")



# df["avgRatingDist"] = df["rating"] - df["rating2"]
# for i in range(7):
#     for j in range(7):
#         if (j >= i):
#             print "(%d, %d)" % (i,j)
#             print df[(df["minDist"] == i) & (df["minDist2"]==j)]["avgRatingDist"].mean()
#             print df[(df["minDist"] == i) & (df["minDist2"]==j)]["avgRatingDist"].shape[0]


show()
