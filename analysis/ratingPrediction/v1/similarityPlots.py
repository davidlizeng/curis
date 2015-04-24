import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
import numpy as np
import math


def plotSimilarity(col, delta, color, title):
    percentiles = range(0, 100, delta)+[100]
    sim_percentiles = np.percentile(df[col], percentiles)

    pos = df[df[r_col] > 0]

    values = []
    means = []
    errors = []
    errors_means = []
    for i in range(len(percentiles) - 1):

        positiveReviews = pos[
            (pos[col] >= sim_percentiles[i])
            & (pos[col] <= sim_percentiles[i+1])
        ].shape[0]

        totalReviews = df[
            (df[col] >= sim_percentiles[i])
            & (df[col] <= sim_percentiles[i+1])
        ].shape[0]

        if totalReviews > 0:
            p = positiveReviews*1.0 / totalReviews
            error = math.sqrt(p*(1-p)/totalReviews)
        else:
            p = 0
            error = 0

        values.append(p)
        errors.append(error)

        ratingsOfInterest = df[
            (df[col] >= sim_percentiles[i])
            & (df[col] <= sim_percentiles[i+1])
        ][r_col]
        means.append(ratingsOfInterest.mean())
        errors_means.append(
            ratingsOfInterest.std()/math.sqrt(ratingsOfInterest.shape[0]))

    x = np.array(percentiles[:-1]) + (delta * .5)

    fig = plt.figure()
    fig.set_facecolor("white")

    p = plt.errorbar(
        x.tolist(),
        values,
        marker="o",
        color=color,
        yerr=errors)

    plt.ylim([0, .5])

    plot(
        plt.xlim(),
        [mean, mean],
        color='black',
        linewidth=1,
        linestyle="--")

    legend([p], [title], loc=4)

    xlabel("Similarity (percentile)")
    ylabel("Fraction of Positive Ratings")

    fig = plt.figure()
    fig.set_facecolor("white")

    p = plt.errorbar(
        x.tolist(),
        means,
        marker="o",
        color=color,
        yerr=errors_means)

    plt.ylim([-1.75, 0])

    plot(
        plt.xlim(),
        [ratingMean, ratingMean],
        color='black',
        linewidth=1,
        linestyle="--")

    legend([p], [title], loc=4)

    xlabel("Similarity (percentile)")
    ylabel("Average Rating")

    return p


df = pd.read_pickle(
    "savedFrames/ratingPrediction/ratingTable")

df["positive"] = df["rating"] > 0
mean = df["positive"].value_counts()[1]*1.0/df["positive"].shape[0]
ratingMean = df["rating"].mean()

#relevant columns
r_col = "rating"
paperSim_col = "pastPaperSimilarity"
userSim_col = "authorReviewerSimilarity"
maxAuthorSim_col = "maxAuthorReviewerSimilarity"
#userSim_col = paperSim_col


plotSimilarity(userSim_col, 5, "Blue",
               "Primary Author / Reviewer Similarity")
plotSimilarity(paperSim_col, 10, "Green",
               "Paper / Reviewer Similarity")
plotSimilarity(maxAuthorSim_col, 5, "#00aaaa",
               "Most Experienced Author / Reviewer Similarity")

plotSimilarity("jaccardSpecificSubjects", 10, "#00aaaa",
               "Subject Similarity")
plotSimilarity("jaccardGeneralSubjects", 10, "#aa00aa",
               "General Subject Similarity")

show()





