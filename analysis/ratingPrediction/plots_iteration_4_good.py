import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
from utilities.plotBucket import plotBucket
from utilities.plotBucket import plotBar
from utilities.plotBucket import plotFrequencyHistogram


df_rating = pd.read_pickle(
    "savedFrames/ratingPrediction/ratingTable")
df_paper = pd.read_pickle(
    "savedFrames/summaryStatistics/papersTable")
df_dist = pd.read_pickle(
    "savedFrames/reviewStatistics/reviewTable")
df_reviewer = pd.read_pickle(
    "savedFrames/summaryStatistics/reviewerTable")
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
                           "maxPageRank",
                           "maxEigenCenter",
                           "maxDegCenter",
                           "primarySpecificSubjectArea",
                           "primarySubjectArea"]],
              on=["paperId"])

#Average Rating vs. Number of Past Papers
p1 = plotBucket(
    df_rating,
    "authorsMaxPastPaper",
    "rating",
    delta=10,
    color="blue",
    x_label="Number of Past Papers",
    y_label="Average Rating")
setp(p1, linewidth=1.5)

p2 = plotBucket(
    df_rating,
    "primaryAuthorPastPaperCount",
    "rating",
    delta=10,
    color="red",
    sameFigure=True,
    marker="s")
setp(p2, linewidth=1.5)
legend([p1, p2], ["Most Experienced Author", "Primary Author"], loc=4)

#Most Experienced Author Reviewer Similarity
maxSimCol = "maxAuthorReviewerSimilarity"

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

#Basic Frequency Plots
plotFrequencyHistogram(
    df,
    "rating",
    "Paper Ratings",
    color="#B9E84D",
    myBins=[-3.6, -2.4, -1.2, 0, 1.2, 2.4, 3.6],
    plotMean=False)
xticks([-3, -1.8, -.6, .6, 1.8, 3],
       ["Strong Reject", "Reject", "Weak Reject",
        "Weak Accept", "Accept", "Strong Accept"])
colors =\
    ["#FF1C00", "#FF5C54", "#FFA6A1", "#A1D3FF", "#54B2FF", "#006FFF"]
for container in plt.gca().containers:
    for i, child in enumerate(container.get_children()):
        child.set_color(colors[i])


plotFrequencyHistogram(
    df_reviewer[df_reviewer["numReviews"] >= 8],
    "avgDeviation",
    "Average Deviation from Paper Mean (at least 8 reviews)",
    color="#E8634D")

#Average Rating vs. Number of Authors given max count
maxPaper = df_paper["authorsMaxPastPaper"]

n = 4
breaks = [0, 25, 100, 200, 900]
slices =\
    [((maxPaper >= breaks[i]) & (maxPaper <= breaks[i+1])) for i in range(n)]

p = plotBucket(
    df_paper,
    "#Authors",
    "avgRating",
    delta=10,
    color="white",
    x_label="Number of Authors",
    y_label="Average Rating",
    marker="None",
    x_percentile=False)

df1 = df_paper.copy()[slices[0]]
ofInterest = df1["#Authors"] >= 3
newValue = np.round(df1[ofInterest]["#Authors"].mean(), 2)
df1.loc[ofInterest, "#Authors"] = newValue
p1 = plotBar(
    df1,
    "#Authors",
    "avgRating",
    [1, 2, newValue],
    color="blue",
    sameFigure=True,
    marker="s",
    plotMean=False)

p2 = plotBucket(
    df_paper[slices[1]],
    "#Authors",
    "avgRating",
    delta=20,
    color="red",
    sameFigure=True,
    x_percentile=False,
    marker="s",
    plotMean=False)

p3 = plotBucket(
    df_paper[slices[2]],
    "#Authors",
    "avgRating",
    delta=20,
    color="green",
    sameFigure=True,
    x_percentile=False,
    marker="s",
    plotMean=False)

p4 = plotBucket(
    df_paper[slices[3]],
    "#Authors",
    "avgRating",
    delta=20,
    color="purple",
    sameFigure=True,
    x_percentile=False,
    marker="s",
    plotMean=False)

legend(
    [p1, p2, p3, p4],
    ["Less than 25 Papers",
     "Between 25 and 100 Papers",
     "Between 100 and 200 Papers",
     "Greater than 200 Papers"],
    loc=4,
    title="Most Experienced Author Paper Count",
    fontsize=12)


p = plotBucket(
    df_paper,
    "#Authors",
    "avgRating",
    delta=15,
    color="brown",
    x_label="Number of Authors",
    y_label="Average Rating",
    x_percentile=False)


#Distance to first four closest authors
p1 = plotBar(
    df,
    "minDist",
    "rating",
    range(7)[1:],
    xlim=[0, 7],
    color="#FF150D",
    x_label="Reviewer Distance to Closest Authors",
    y_label="Avg Rating",
    errorBars=False,
)
p2 = plotBar(
    df,
    "secondMinDist",
    "rating",
    range(7)[1:],
    color="purple",
    sameFigure=True,
    errorBars=False,
)
p3 = plotBar(
    df,
    "thirdMinDist",
    "rating",
    range(7)[1:],
    color="#2A00FF",
    sameFigure=True,
    errorBars=False,
)
p4 = plotBar(
    df,
    "fourthMinDist",
    "rating",
    range(7)[1:],
    color="green",
    sameFigure=True,
    errorBars=False,
)

setp(p1, linewidth=4.5, alpha=.7)
setp(p2, linewidth=4.5, alpha=.7)
setp(p3, linewidth=4.5, alpha=.7)
setp(p4, linewidth=4.5, alpha=.7)
legend([p1, p2, p3, p4], [
    "Distance to Closest Author (Min)",
    "Distance to Second Closest Author",
    "Distance to Third Closest Author",
    "Distance to Fourth Closest Author"], loc=3,
    fontsize=12)


#Average Accepted

authorFrame = userFrame[userFrame["#Papers"] > 0]
authorFrame.loc[
    (authorFrame["#Papers"] >= 6) & (authorFrame["#Papers"] <= 10),
    "#Papers"] = 6
authorFrame.loc[authorFrame["#Papers"] >= 11, "#Papers"] = 7

plotBar(
    authorFrame,
    "#Papers",
    "#Accepted",
    range(8),
    title="Average Number of Accepted vs. Number of Submissions",
    x_label="Number of Submissions",
    y_label="Average Number Accepted",
    xlim=[0, 8]
)
xticks([1, 2, 3, 4, 5, 6, 7],
       [1, 2, 3, 4, 5, "(6 - 10)", "11+"])

#Connectivity
plotBucket(
    papersFrame,
    "maxConnectivity",
    "avgRating",
    x_label="Connectivity of Most Connected Author",
    y_label="Average Rating",
    title="Connectivity in a Co-authorship Graph",
    delta=10,
    x_percentile=False,
)
gca().set_xscale('log')


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
    #xlim=[50, 100000]
)
gca().set_xscale('log')
plt.plot(x, yfit, 'k--')

#Page Rank
plotBucket(
    papersFrame,
    "maxPageRank",
    "avgRating",
    x_label="Max PageRank of Authors",
    y_label="Average Rating",
    title="Connectivity in a Co-authorship Graph",
    delta=10,
    x_percentile=False,
)
gca().set_xscale('log')

dfconn = df[df["maxPageRank"] > 0]
xs = np.log(dfconn["maxPageRank"].values)
A = array([xs, ones(len(xs))])
ys = dfconn[maxSimCol].values

w = np.linalg.lstsq(A.T, ys)[0]
x = np.logspace(-7, -4, 100)
yfit = w[0]*np.log(x) + w[1]

plotBucket(
    dfconn,
    "maxPageRank",
    maxSimCol,
    x_label="Max PageRank of Authors",
    y_label="Similarity between Author and Reviewer",
    title="Similarity vs. Connectivity",
    delta=5,
    x_percentile=False,
    plotMean=False,
    #xlim=[50, 100000]
)
gca().set_xscale('log')
plt.plot(x, yfit, 'k--')

#Degree Centrality
plotBucket(
    papersFrame,
    "maxDegCenter",
    "avgRating",
    x_label="Max Degree Centrality of Authors",
    y_label="Average Rating",
    title="Connectivity in a Co-authorship Graph",
    delta=10,
    x_percentile=False,
)
gca().set_xscale('log')

dfconn = df[df["maxDegCenter"] > 0]
xs = np.log(dfconn["maxDegCenter"].values)
A = array([xs, ones(len(xs))])
ys = dfconn[maxSimCol].values

w = np.linalg.lstsq(A.T, ys)[0]
x = np.logspace(-6, -3, 100)
yfit = w[0]*np.log(x) + w[1]

plotBucket(
    dfconn,
    "maxDegCenter",
    maxSimCol,
    x_label="Max Degree Centrality of Authors",
    y_label="Similarity between Author and Reviewer",
    title="Similarity vs. Connectivity",
    delta=5,
    x_percentile=False,
    plotMean=False,
    #xlim=[50, 100000]
)
gca().set_xscale('log')
plt.plot(x, yfit, 'k--')

dfconn = df[(df["maxConnectivity"] > 0) & (df["maxPageRank"] > 0) &\
     & (df["maxDegCenter"] > 0)]
xs = np.log(dfconn[["maxConnectivity", "maxPageRank", "maxDegCenter"]].values).T
A = np.vstack((xs, ones(xs.shape[1])))

ys = dfconn[maxSimCol].values

fit = sm.OLS(ys, A.T).fit()
fit.summary()

#Review Length
df["agreement"] = (df["rating"] > 0) == df["accepted"]
plotBucket(
    df,
    "reviewLength",
    "agreement",
    delta=10,
    x_percentile=False,
    xlim=[0, 600],
    x_label="Review Length",
    y_label="Proportion of Reviews that Agree with Acceptance",
    title="Review Influence")

df["absrating"] = df["rating"].abs()
plotBucket(
    df,
    "reviewLength",
    "absrating",
    delta=10,
    x_percentile=False,
    xlim=[0, 600],
    x_label="Review Length",
    y_label="Average Rating (Absolute Value)",
    title="Rating Magnitude vs. Review Length")


p = plotBar(
    df,
    "reviewerCountry",
    "reviewLength",
    [
    "USA",
    "China",
    "Germany",
    "Singapore",
    "Taiwan",
    "Australia",
    "Japan",
    "Canada"
    ],
    title="Review Length by Reviewer Country",
    x_label="Reviewer Country",
    y_label="Average Review Length",
    categorical=True
)
colors =\
    ["#334D5C", "#45B29D", "#EFC94C", "#E27A3F",
     "#DF4949", "#5FAAA5", "#649C57", "#F6A52E"]
j = 0
for container in plt.gca().containers:
    for i, child in enumerate(container.get_children()):
        print i
        if j > 3:
            child.set_color(colors[i])
        j += 1

plotFrequencyHistogram(
    df,
    "reviewLength",
    "Length of Reviews",
    plotMean=True,
    myBins=np.linspace(0, 2500, 20))
ylim([0, 1200])

df["agreement"] = (df["rating"] > 0) == df["accepted"]
plotBar(
    df,
    "rating",
    "agreement",
    [-3, -2, -1, 1, 2, 3],
    x_label="Rating",
    y_label="Proportion of Reviews that Agree with Acceptance",
    title="Review Influence by Rating",
    categorical=True)
xticks(range(6),
       ["Strong Reject", "Reject", "Weak Reject",
       "Weak Accept", "Accept", "Strong Accept"])

colors =\
    ["#FF1C00", "#FF5C54", "#FFA6A1", "#A1D3FF", "#54B2FF", "#006FFF"]
j = 0
for container in plt.gca().containers:
    for i, child in enumerate(container.get_children()):
        if j > 3:
            child.set_color(colors[i])
        j += 1

noExternal = df[df["externalReviewer"] == ""]["reviewLength"]
external = df[df["externalReviewer"] != ""]["reviewLength"]
numNoExternal = df[df["externalReviewer"] == ""].shape[0]
numExternal = df[df["externalReviewer"] != ""].shape[0]

x = [0, 1]
y = [noExternal.mean(), external.mean()]
yerr = (
    noExternal.std()/math.sqrt(noExternal.shape[0]),
    external.std()/math.sqrt(external.shape[0]))

plt.figure(facecolor="white")
gca().bar(x, y, yerr=yerr, ecolor="black")
ylabel("Review Length")
text(0.4, 420, numNoExternal, color="gray", ha="center")
text(1.4, 420, numExternal, color="gray", ha="center")
text(0.9, 400, "(Number of Reviews)", color="gray", ha="center")

xticks([.4, 1.4], ["Assigned Reviewers", "External Reviewers"])
xlim([-.2, 2])
ylim([0, 450])
plt.suptitle("Comparing Review Length of External Reviewers")

j = 0
colors = ["#94B6FF", "#FF8574"]
for container in plt.gca().containers:
    for i, child in enumerate(container.get_children()):
        if j > 3:
            child.set_color(colors[i])
        j += 1

#Top Conferences
p1 = plotBucket(
    df_rating,
    "authorsMaxPastPaper",
    "rating",
    delta=10,
    color="blue",
    x_label="Number of Past Papers",
    y_label="Average Rating",
    title="Distinguishing where the papers were published")

p2 = plotBucket(
    df_rating,
    "maxTopCount",
    "rating",
    delta=10,
    color="green",
    sameFigure=True)

p3 = plotBucket(
    df_rating,
    "maxKDDCount",
    "rating",
    delta=10,
    color="purple",
    sameFigure=True)

legend([p1, p2, p3], ["All Papers", "Top Conferences", "KDD"], loc=4,
       title="Past Paper Count of Most Experienced Author")

#Top Conferences
p1 = plotBucket(
    df_rating,
    "authorsMaxPastPaper",
    "rating",
    numBuckets=7,
    color="blue",
    x_label="Number of Past Papers in Top Conferences",
    y_label="Average Rating",
    title="NEED TITLE",
    x_percentile=False)

p2 = plotBucket(
    df_rating,
    "priTopCount",
    "rating",
    numBuckets=7,
    color="green",
    sameFigure=True,
    x_percentile=False)

legend([p1, p2], ["Most Exp Author", "Primary Author"], loc=4)


p1 = plotBucket(
    df_rating,
    "maxTopCount",
    "rating",
    delta=10,
    color="green",
    x_percentile=False,
    x_label="Number of Past Papers in Top Conferences and Journals",
    title="Rating vs. Publishing in Top Publications",
    y_label="Average Rating",
    xlim=[0, 75]
)

p2 = plotBucket(
    df_rating,
    "maxKDDCount",
    "rating",
    x_percentile=False,
    delta=5,
    color="purple",
    x_label="Number of Past Papers in KDD",
    title="Rating vs. Publishing in KDD",
    y_label="Average Rating",
    sameFigure=True
)
legend([p1, p2], ["All Top Journals/Conferences", "Just KDD"], loc=4,
       title="Past Paper Count of Most Experienced Author")

plotFrequencyHistogram(
    df_rating,
    "maxKDDCount",
    "Past Publications in KDD of Most Experienced Author",
    myBins=[0, 1, 2, 3, 5, 10, 20, 30, 40, 50, 60]
)
xticks([0, 1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60])
xlim([-3, 60])

show()
