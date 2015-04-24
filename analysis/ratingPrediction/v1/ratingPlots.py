import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
import numpy as np
import math


def plotBucket(
        df, xcol, ycol, delta, color, title, x_label, y_label, x_percentile):

    percentiles = range(0, 100, delta)+[100]
    col_percentiles = np.percentile(df[xcol], percentiles)

    values = []
    errors = []
    for i in range(len(percentiles) - 1):
        ratingsOfInterest = df[
            (df[xcol] >= col_percentiles[i])
            & (df[xcol] <= col_percentiles[i+1])
        ][ycol]

        values.append(ratingsOfInterest.mean())
        errors.append(
            ratingsOfInterest.std()/math.sqrt(ratingsOfInterest.shape[0])
        )

    if x_percentile:
        x = np.array(percentiles[:-1]) + (delta * .5)
    else:
        x = []
        for i in range(len(col_percentiles) - 1):
            x.append((col_percentiles[i] + col_percentiles[i+1])/2)

    fig = plt.figure()
    fig.set_facecolor("white")

    plt.errorbar(
        x,
        values,
        marker="o",
        color=color,
        yerr=errors)

    plot(
        plt.xlim(),
        [df[ycol].mean(), df[ycol].mean()],
        color='black',
        linewidth=1,
        linestyle="--")
    print df[ycol].mean()

    plt.suptitle(title)

    xlabel(x_label)
    ylabel(y_label)

    if ycol == "rating":
        plt.ylim([-2.25, 0.25])


df = pd.read_pickle(
    "savedFrames/ratingPrediction/ratingTable")
df_papers = pd.read_pickle(
    "savedFrames/summaryStatistics/papersTable")

r_col = "rating"

# plotBucket(
#     "specificCommonSubjects",
#     10,
#     "blue",
#     "Average Rating vs. Number of Common Subjects",
#     "Number of Common Subjects",
#     False)

# plotBucket(
#     "reviewerPastPaperCount",
#     5,
#     "blue",
#     "Average Rating vs. Reviewer's Past Paper Count",
#     "Reviewer's Past Paper Count",
#     True)

# plotBucket(
#     df,
#     "authorsMaxPastPaper",
#     "rating",
#     5,
#     "blue",
#     "Average Rating vs. Number of Past Papers of Most Experienced Author",
#     "Number of Papers (Percentile)",
#     "Average Rating",
#     True)
# plotBucket(
#     "authorsMaxPastPaper",
#     "rating",
#     5,
#     "blue",
#     "Average Rating vs. Number of Past Papers of Most Experienced Author",
#     "Number of Papers",
#     "Average Rating",
#     False)

# plotBucket(
#     df,
#     "primaryAuthorPastPaperCount",
#     "rating",
#     5,
#     "green",
#     "Average Rating vs. Number of Past Papers of Primary Author",
#     "Number of Papers (Percentile)",
#     "Average Rating",
#     True)
# plotBucket(
#     df,
#     "primaryAuthorPastPaperCount",
#     "reviewerRatingDiff",
#     5,
#     "green",
#     "Deviation from Reviewer's Average Rating for Primary Author",
#     "Number of Papers (Percentile)",
#     "Deviation Average Rating",
#     True)
# plotBucket(
#     "primaryAuthorPastPaperCount",
#     "rating",
#     5,
#     "green",
#     "Average Rating vs. Number of Past Papers of Primary Author",
#     "Number of Papers",
#     "Average Rating",
#     False)

# plotBucket(
#     df,
#     "authorsMaxPastPaper",
#     "reviewerRatingDiff",
#     5,
#     "blue",
#     "Deviation from Reviewer's Average Rating for Experienced Authors",
#     "Number of Papers (Percentile)",
#     "Deviation from Average Rating",
#     True)

# plotBucket(
#     df_papers,
#     "authorsMaxPastPaper",
#     "accepted",
#     10,
#     "blue",
#     "P(Accept) vs. Number of Past Papers of Most Experienced Author",
#     "Number of Papers (Percentile)",
#     "P(Accept)",
#     True)

plotBucket(
    df,
    "authorReviewerSimilarity",
    "rating",
    5,
    "#606000",
    "Average Rating vs. Author / Reviewer Similarity",
    "Similarity (Percentile)",
    "Average Rating",
    False)
# plotBucket(
#     df,
#     "authorReviewerSimilarity",
#     "reviewerRatingDiff",
#     5,
#     "#606000",
#     "Deviation from Reviewer Average vs. Author / Reviewer Similarity",
#     "Similarity (Percentile)",
#     "Deviation from Reviewer Average Rating",
#     True)
# plotBucket(
#     df,
#     "authorReviewerSimilarity",
#     "paperRatingDiff",
#     5,
#     "#606000",
#     "Deviation from Paper Average vs. Author / Reviewer Similarity",
#     "Similarity (Percentile)",
#     "Deviation from Paper Average Rating",
#     True)

df["abovePaperAverage"] = df["rating"] > df["paperAverage"]
plotBucket(
    df,
    "authorReviewerSimilarity",
    "abovePaperAverage",
    5,
    "#a0a040",
    "Probability of Review above Paper Average / Reviewer Similarity",
    "Similarity (Percentile)",
    "Probability of Rating above Paper Average",
    False
    )

plotBucket(
    df,
    "maxAuthorReviewerSimilarity",
    "rating",
    5,
    "#00aaaa",
    "Average Rating vs. Most Experienced Author / Reviewer Similarity",
    "Similarity (Percentile)",
    "Average Rating",
    False)


plotBucket(
    df,
    "primaryAuthorPastPaperCount",
    "authorReviewerSimilarity",
    5,
    "red",
    "Author / Reviewer Similarity vs Past Paper count",
    "Past Paper Count",
    "Similarity",
    False)

plt.scatter(df["primaryAuthorPastPaperCount"], df["authorReviewerSimilarity"], alpha = .5)
xlim([0, 50])


plotBucket(
    df,
    "primaryAuthorPastPaperCount",
    "authorReviewerSimilarity",
    5,
    "red",
    "Author / Reviewer Similarity vs Past Paper count",
    "Past Paper Count",
    "Similarity",
    False)

plt.scatter(df["primaryAuthorPastPaperCount"], df["authorReviewerSimilarity"], alpha = .5)
xlim([0, 200])
# plotBucket(
#     df,
#     "maxAuthorReviewerSimilarity",
#     "reviewerRatingDiff",
#     5,
#     "#00aaaa",
#     "Dev. from Reviewer Avg. vs. Most Experienced Author / Reviewer Similarity",
#     "Similarity (Percentile)",
#     "Deviation from Reviewer Average Rating",
#     True)

# plotBucket(
#     df,
#     "jaccardSpecificSubjects",
#     "rating",
#     10,
#     "#aa00aa",
#     "Rating vs. Jaccard Similarity of Specific Subject Areas",
#     "Similarity",
#     "Average Rating",
#     False)

# plotBucket(
#     df,
#     "jaccardGeneralSubjects",
#     "rating",
#     10,
#     "#ff00ff",
#     "Rating vs. Jaccard Similarity of Gpecific Subject Areas",
#     "Similarity",
#     "Average Rating",
#     False)

show()

#def plotAvgRating(
#        xcol, ycol, delta, color, title, x_label, y_label, x_percentile):
