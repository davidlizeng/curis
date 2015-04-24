import warnings
import numpy as np
import datetime
from pylab import *
from scipy.interpolate import spline
from feature_extraction import calcFeatures
from utilities.plotBucket import setUpFigure
from utilities.plotBucket import plotBucket
from utilities.dates import *
from scipy.stats import percentileofscore

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from pandas import DataFrame

from feature_extraction.dataLoader import DataLoader

loader = DataLoader()
loader.loadUsers()
loader.loadPapers()
loader.loadPastPapers()
loader.loadAcceptance()
loader.loadReviews()
loader.loadClassifierAccuracy()
calcFeatures.computeAverages(loader)

reviewerTable = []

oneDayBefore = int(datetime.datetime(2014, 4, 14, 0, 0, 0).strftime('%s'))
deadline = int(datetime.datetime(2014, 4, 15, 0, 0, 0).strftime('%s'))

for id, reviewer in loader.reviewers.iteritems():
    revs = reviewer.reviews
    if len(revs) > 0:

        deviations = np.array([
            r.overallRating - r.paper.avgRating
            for r in revs])

        numExtreme = 0
        for r in revs:
            devs = np.array([
                abs(r2.overallRating - r.paper.avgRating)
                for r2 in r.paper.reviews
            ])

            if abs(r.overallRating - r.paper.avgRating) == devs.max():
                if devs.max() > 1:
                    numExtreme += 1

        submissionTimes = np.array([
            int(r.time.strftime('%s'))
            for r in revs])
        averageTime = np.datetime64(
            datetime.datetime.fromtimestamp(
                submissionTimes.mean()
            )
        ),
        inLastDay = np.array([
            1 for t in submissionTimes
            if t < deadline and t >= oneDayBefore])
        afterDeadline = np.array([
            1 for t in submissionTimes
            if t >= deadline])

        externalReviews = np.array([
            1 if len(r.externalReviewer) > 0 else 0
            for r in revs])
        influence = np.array([
            1 if ((r.overallRating > 0) == r.paper.accepted) else 0
            for r in revs])

        accuracy = np.array([
            r.classifierAccAccept
            for r in revs])

        length = np.array([
            len(r.getReviewText().split())
            for r in revs])

        if len(reviewer.reviews) > 0:
            reviewerStats = {
                "userId": id,

                #report stats
                "numberOfBids": len(reviewer.bids),
                "numberOfReviews": len(reviewer.reviews),
                "paperDeviation": deviations.mean(),  # Done
                "externalReviews": externalReviews.sum(),
                "extreme": numExtreme,
                #eval criteria
                "subTime": np.datetime64(
                    datetime.datetime.fromtimestamp(
                        submissionTimes.mean())),
                "subLastDay": inLastDay.sum(),  # Done
                "subLate": afterDeadline.sum(),
                "influence": influence.mean(),  # Done
                "accuracy": accuracy.mean(),  # Done
                "length": length.mean()  # Done

            }
        reviewerTable.append(reviewerStats)

df = DataFrame(reviewerTable)


#plot cdf
def plotCDF(
        df,
        col,
        x_label,
        title=None,
        x_lim=None,
        color="blue"):

    y = np.linspace(0, 100, 200)
    x = np.percentile(df[col].values, list(y))

    xForLim = np.percentile(df[col].values, [10, 90])
    delta = (xForLim[1] - xForLim[0])/3.0
    x_low = xForLim[0] - delta
    x_high = xForLim[1] + delta

    y = y/100

    setUpFigure(
        x_label,
        "CDF of Reviewers",
        title if title is not None else "CDF of %s" % x_label,
        xlim=(x_low, x_high),
        ipython=False
    )

    plot(
        x,
        y,
        alpha=.7,
        color=color,
        linewidth=3)

    ylim(0, 1)

    if x_lim is not None:
        xlim(x_lim)

    plot(
        xlim(),
        [.5, .5],
        color="black",
        linestyle="--"
    )


# plotCDF(
#     df,
#     "length",
#     "Review Length (Words)",
#     title="Average Review Length Distribution"
# )

# plotCDF(
#     df,
#     "influence",
#     "Reviewer Influence (Proportion of Reviews that Agree with Acceptance)",
#     title="Distribution of Reviewer Influence",
#     x_lim=[0, 1]
# )

# plotCDF(
#     df,
#     "accuracy",
#     "Classification Accuracy",
#     title="Distribution of Classification Accuracy",
#     x_lim=[.4, 1]
# )

# plotCDF(
#     df,
#     "subLastDay",
#     "Number of Last Day Submissions",
#     title="Distribution of Number of Last Day Submissions",
#     x_lim=[-.5, 9]
# )

# plotCDF(
#     df,
#     "paperDeviation",
#     "Average Deviation from Paper Average",
#     "Distribution of Average Deviation from Paper Average"
# )

# plotCDF(
#     df,
#     "subLate",
#     "Number of Late Submissions",
#     title="Distribution of Number of Late Submissions",
#     x_lim=[-.5, 10]
# )


# df['subTime'] = df['subTime'].values.astype(datetime.datetime)
# dateLabels = ["3/31", "4/5", "4/10", "4/15", "4/20", "4/25", "4/30"]
# dates = transformDates(dateLabels)
# plotCDF(
#     df,
#     "subTime",
#     "Average Submission Time",
#     title="Distribution of Submission Times",
#     x_lim=[dates[0], dates[-1]]
# )
# xticks(dates, dateLabels)
# plotDeadline(.9)


# show()

###restrict to reviewers with at least 7 reviews
df = df[df["numberOfReviews"] >= 7]

a = df["length"].values
df["rankingLength"] = df.apply(lambda x: percentileofscore(a, x["length"]), axis=1)
a = df["influence"].values
df["rankingInfluence"] = df.apply(lambda x: percentileofscore(a, x["influence"]), axis=1)
a = df["accuracy"].values
df["rankingAccuracy"] = df.apply(lambda x: percentileofscore(a, x["accuracy"]), axis=1)

# df["lateScore"] = (.5*df["subLastDay"] + df["subLate"])/df["numberOfReviews"]
# a = df["lateScore"].values
# df["rankingLate"] = df.apply(lambda x: percentileofscore(a, x["lateScore"]), axis=1)

# df["rankingScore"] =\
#     .5*df["rankingLength"]\
#     + .3*df["rankingInfluence"]\
#     + .2*df["rankingAccuracy"]\
#     - df["rankingLate"]
df["rankingScore"] =\
    df["rankingLength"]\
    + df["rankingInfluence"]\
    + df["rankingAccuracy"]

#a = df["rankingScore"].values
#df["ranking"] = df.apply(lambda x: percentileofscore(a, x["rankingScore"]), axis=1)

f = open("csv/reviewerStatistics.csv", 'wb')
for index, row in df.iterrows():
    f.write("%d, %s, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n" % (
        row["userId"],
        loader.users[row["userId"]].name,
        row["rankingScore"],
        row["rankingLength"],
        row["length"],
        row["rankingInfluence"],
        row["influence"],
        row["rankingAccuracy"],
        row["accuracy"],
        # row["rankingLate"],
        # row["subLastDay"],
        # row["subLate"]
        row["numberOfBids"],
        row["numberOfReviews"],
        row["externalReviews"],
        row["extreme"]
    ))
f.close()

