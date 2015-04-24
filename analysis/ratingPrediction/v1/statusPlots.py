import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
import numpy as np
import math


def plotStatus(col, delta, color, title):

    percentiles = range(0, 100, delta)+[100]
    status_percentiles = np.percentile(df[col], percentiles)

    values = []
    errors = []
    for i in range(len(percentiles) - 1):
        ratingsOfInterest = df[
            (df[col] >= status_percentiles[i])
            & (df[col] <= status_percentiles[i+1])
        ][r_col]

        values.append(ratingsOfInterest.mean())
        errors.append(
            ratingsOfInterest.std()/math.sqrt(ratingsOfInterest.shape[0])
        )

    x = []
    for i in range(len(status_percentiles) - 1):
        x.append((status_percentiles[i] + status_percentiles[i+1])/2)

    fig = plt.figure()
    fig.set_facecolor("white")

    plt.ylim([-1.5, 0])
    plt.xlim([-500, 300])

    p = plt.errorbar(
        x,
        values,
        marker="o",
        color=color,
        yerr=errors)

    plot(
        plt.xlim(),
        [df[r_col].mean(), df[r_col].mean()],
        color='black',
        linewidth=1,
        linestyle="--")

    plot(
        [0, 0],
        plt.ylim(),
        color='red',
        linewidth=.5,
        linestyle="--")

    plt.suptitle(title)

    xlabel("Status Difference")
    ylabel("Average Rating")


df = pd.read_pickle(
    "savedFrames/ratingPrediction/ratingTable")


df["status1"] = df["reviewerPastPaperCount"] - df["primaryAuthorPastPaperCount"]
df["status2"] = df["reviewerPastPaperCount"] - df["authorsMaxPastPaper"]
r_col = "rating"

plotStatus(
    "status1",
    8,
    "blue",
    "Status Difference between Reviewer and Primary Author")

plotStatus(
    "status2",
    8,
    "green",
    "Status Difference between Reviewer and Most Experienced Author")


show()