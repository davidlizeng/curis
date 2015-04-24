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
userFrame = pd.read_pickle(
    "savedFrames/summaryStatistics/userTable")
df_mostSimilar = pd.read_pickle(
    "savedFrames/ratingPrediction/mostSimilarTable")
df_merged = pd.merge(df_rating, df_dist, on=['paperId', 'userId', 'rating'])
df_merged = pd.merge(df_merged, df_mostSimilar, on=['paperId'])

#Plot past paper count vs. average rating
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


#Plot Past paper count vs. P(Accept)
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


#Plot co-author dist
p1 = plotBucket(
    df_merged,
    "avgDist",
    "rating",
    delta=10,
    x_label="Reviewer Author Distance",
    y_label="Avg Rating",
    xlim=[0, 8],
    x_percentile=False
)
p2 = plotBar(
    df_merged,
    "minDist",
    "rating",
    range(7)[1:],
    color="red",
    sameFigure=True,
)

legend([p1, p2],
       ["Average Author Distance",
       "Min Author Distances"])


#Plot min co-author dist vs P(Accept)
g = df_merged.groupby('paperId')
h = pd.concat([
    g["minDist"].mean(),
    g["minDist"].min(),
    g["accepted"].median()], axis=1)
h.columns = [
    "avgMinDist",
    "minMinDist",
    "accepted"]

p1 = plotBucket(
    h,
    "avgMinDist",
    "accepted",
    delta=20,
    x_label="Reviewer Author Distance",
    y_label="P(Accept)",
    xlim=[1, 7],
    x_percentile=False
)

p2 = plotBucket(
    h,
    "minMinDist",
    "accepted",
    delta=15,
    color="red",
    sameFigure=True,
    x_percentile=False
)

legend([p1, p2],
       ["Average of Min Distance",
       "Min of Min Distances"])


#First Closest Author vs. Second Closest Author
p1 = plotBar(
    df_merged,
    "secondMinDist",
    "rating",
    range(7)[1:],
    xlim=[0, 7],
    color="black",
    x_label="Reviewer Distance to Closest Authors",
    y_label="Avg Rating"
)
p2 = plotBar(
    df_merged,
    "minDist",
    "rating",
    range(7)[1:],
    color="red",
    sameFigure=True,
)
legend([p2, p1], [
    "Distance to Closest Author (Min)",
    "Distance to Second Closest Author"], loc=3)


#Second Closest Author Conditioned on First
def plotCondSecond(df, num, color, first):
    df_cond = df[df["minDist"] == num]
    return plotBar(
        df_cond,
        "secondMinDist",
        "rating",
        range(7)[num:],
        color=color,
        x_label="Reviewer Distance to Second Closest Author",
        y_label="Avg Rating",
        sameFigure=(not first),
        plotMean=False
    )
p1 = plotCondSecond(df_merged, 1, "blue", True)
p2 = plotCondSecond(df_merged, 2, "red", False)
p3 = plotCondSecond(df_merged, 3, "purple", False)
p4 = plotCondSecond(df_merged, 4, "green", False)
legend([p1, p2, p3, p4], [
    "Given Min Dist = 1",
    "Given Min Dist = 2",
    "Given Min Dist = 3",
    "Given Min Dist = 4"], loc=3)

#Most Experienced Author Reviewer Similarity
maxSimCol = "maxAuthorReviewerSimilarity"

plotBucket(
    df_merged,
    maxSimCol,
    "rating",
    x_label="Similarity",
    y_label="Rating",
    title=
    "Average Rating vs. Similarity of Reviewer to Most Experienced Author",
    color="green"
)

plotBucket(
    df_merged,
    maxSimCol,
    "accepted",
    x_label="Similarity",
    y_label="P(Accept)",
    title=
    "P(Accept) vs. Similarity of Reviewer to Most Experienced Author",
    color="green"
)

plotBucket(
    df_merged,
    maxSimCol,
    "rating",
    x_label="Similarity",
    y_label="Rating",
    delta=10,
    title=
    "Average Rating vs. Similarity of Reviewer to Most Experienced Author",
    color="green",
    xlim=[0, 100]
)

plotBucket(
    df_merged,
    maxSimCol,
    "paperRatingDiff",
    x_label="Max Author Reviewer Similarity",
    y_label="Deviation from Paper Average",
    delta=25,
    color="purple",
    xlim=[0, 100]
)

df_merged["simRatio"] =\
    df_merged[maxSimCol] / df_merged["bestSimilarityOfReviewers"]

plotBucket(
    df_merged,
    "simRatio",
    "rating",
    x_label="Similarity Ratio",
    y_label="Rating",
    delta=7,
    title=
    "Avg. Rating vs. Ratio of Similarity to Reviewer to Most Similar Reviewer",
    color="#00aaaa",
    x_percentile=False
)

df_merged["simRatio"] =\
    df_merged[maxSimCol] / df_merged["bestSimilarityOfAuthors"]

plotBucket(
    df_merged,
    "simRatio",
    "rating",
    delta=7,
    x_label="Similarity Ratio",
    y_label="Rating",
    title=
    "Average Rating vs. Ratio of Similarity to Reviewer to Most Similar User",
    color="#aa00aa",
    x_percentile=False
)





#Acceptance Rate Plot

authorFrame = userFrame[userFrame["#Papers"] > 0]
authorFrame["acceptanceRate"] = authorFrame["#Accepted"] \
    * 1.0/authorFrame["#Papers"]
authorFrame.loc[
    (authorFrame["#Papers"] >= 6) & (authorFrame["#Papers"] <= 10),
    "#Papers"] = 6
authorFrame.loc[authorFrame["#Papers"] >= 11, "#Papers"] = 7

plotBar(
    authorFrame,
    "#Papers",
    "acceptanceRate",
    range(8),
    title="Acceptance Rate vs. Number of Submissions",
    x_label="Number of Submissions",
    y_label="Acceptance Rate",
    xlim=[0, 8]
)
xticks([1, 2, 3, 4, 5, 6, 7],
       [1, 2, 3, 4, 5, "(6 - 10)", "11+"])


#Status Plots
df_merged["status_max"] =\
    df_merged["reviewerPastPaperCount"] - df_merged["authorsMaxPastPaper"]
df_merged["status_primary"] =\
    df_merged["reviewerPastPaperCount"] -\
    df_merged["primaryAuthorPastPaperCount"]

p1 = plotBucket(
    df_merged,
    "status_max",
    "rating",
    delta=8,
    color="#ff5500",
    title="Average Rating vs. Status Difference between Reviewer and Author",
    x_label="Status Difference (Reviewer - Author)",
    y_label="Average Rating",
    x_percentile=False
)
p2 = plotBucket(
    df_merged,
    "status_primary",
    "rating",
    delta=10,
    color="#4422ff",
    x_percentile=False,
    sameFigure=True
)
plot(
    [0, 0],
    plt.ylim(),
    color='red',
    linewidth=.5,
    linestyle="--")
legend([p1, p2], ["Most Experienced Author", "Primary Author"], loc=3)

simPercentiles = np.percentile(df_merged[maxSimCol], [100.0/3, 200.0/3])
lowSim = df_merged[
    df_merged[maxSimCol] <= simPercentiles[0]]
medSim = df_merged[
    (df_merged[maxSimCol] > simPercentiles[0])
    & (df_merged[maxSimCol] <= simPercentiles[1])]
highSim = df_merged[
    df_merged[maxSimCol] > simPercentiles[1]]

p1 = plotBucket(
    highSim,
    "status_max",
    "rating",
    delta=20,
    color="#10a010",

    title="Avgerage Rating vs Status Difference\n"
    + "between Reviewer and Most Experienced Author",

    x_label="Status Difference (Reviewer - Author)",
    y_label="Average Rating",
    x_percentile=False,
    plotMean=False
)
p2 = plotBucket(
    medSim,
    "status_primary",
    "rating",
    delta=15,
    color="#10d0d0",
    x_percentile=False,
    sameFigure=True,
    plotMean=False
)
p3 = plotBucket(
    lowSim,
    "status_primary",
    "rating",
    delta=15,
    color="#1010f0",
    x_percentile=False,
    sameFigure=True,
    plotMean=False
)
plot(
    [0, 0],
    plt.ylim(),
    color='red',
    linewidth=.5,
    linestyle="--")
legend(
    [p1, p2, p3],
    ["High Similarity", "Medium Similarity", "Low Similarity"],
    loc=3)

#Basic Frequency Plots
plotFrequencyHistogram(
    df_rating,
    maxSimCol,
    "Most Experienced Author / Reviewer Similarity",
    color="#62FFBB",
    myBins=None)

plotFrequencyHistogram(
    df_paper,
    "avgRating",
    "Average Rating for a Paper",
    color="#B9E84D",
    myBins=np.arange(-3, 3.5, .5))

plotFrequencyHistogram(
    df_paper,
    "authorsMaxPastPaper",
    "Past Paper Count of Most Experienced Author",
    color="#E8634D",
    myBins=None)

plotFrequencyHistogram(
    userFrame,
    "#PastPapers",
    "Past Paper Count of Users",
    color="#FFCD62",
    myBins=None)

plotFrequencyHistogram(
    userFrame[userFrame["#PastPapers"] < 100],
    "#PastPapers",
    "Past Paper Count (< 100) of Users",
    color="#DE88FF",
    myBins=None)

plotFrequencyHistogram(
    df_merged[df_merged["minDist"] < 7],
    "avgDist",
    "Average Distance in Coauthor Graph between Reviewer and Authors",
    color="#65D3E8",
    myBins=None)

plotFrequencyHistogram(
    df_merged[df_merged["minDist"] < 7],
    "minDist",
    "Minimum Distance in Coauthor Graph between Reviewer and Authors",
    color="#83FF7B",
    myBins=np.arange(.5, 7.5, 1))

plotFrequencyHistogram(
    df_merged,
    "reviewerAverage",
    "Average Rating for a Reviewer",
    color="#DF4949",
    myBins=None)


#Activity vs. Similarity
plotBucket(
    df_merged,
    "authorsMaxPastPaper",
    maxSimCol,
    color="black",
    x_label="Most Experienced Author Past Paper Count",
    y_label="Similarity to Reviewer",
    title="Similarity vs. Activity",
    marker=None,
    xlim=([-20, 400]),
    x_percentile=False
)
scatter(
    df_merged["authorsMaxPastPaper"],
    df_merged[maxSimCol],
    c="#00B26F",
    alpha=.1
)
ylim([0, 1])



plotBucket(
    df_merged,
    "authorsMaxPastPaper",
    maxSimCol,
    color="black",
    x_label="Most Experienced Author Past Paper Count",
    y_label="Similarity to Reviewer",
    title="Similarity vs. Activity",
    marker=None,
    xlim=([-5, 150]),
    x_percentile=False
)
scatter(
    df_merged["authorsMaxPastPaper"],
    df_merged[maxSimCol],
    c="#E25800",
    alpha=.2
)
ylim([0, 1])


#Reviewer Countries
reviewerCountries = [
    "USA",
    "China",
    "Germany",
    "Singapore",
    "Taiwan",
    "Australia",
    "Japan",
    "Canada"]

plotBar(
    df_merged,
    "reviewerCountry",
    "rating",
    reviewerCountries,
    color="#758FFF",
    categorical=True,
    x_label="Reviewer Country",
    y_label="Average Rating",
    title="Average Rating by Reviewer Country")

df_merged["reviewerCountryCount"] = 0
for country in reviewerCountries:
    ofInterest = df_merged["reviewerCountry"] == country
    count = df_merged[ofInterest].shape[0]
    df_merged.loc[ofInterest, "reviewerCountryCount"] = count

plotBar(
    df_merged,
    "reviewerCountry",
    "reviewerCountryCount",
    reviewerCountries,
    color="#75FF8F",
    categorical=True,
    x_label="Reviewer Country",
    y_label="Number of Reviews",
    title="Nationality of Reviewers")



show()