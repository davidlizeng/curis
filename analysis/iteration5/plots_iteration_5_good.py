import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
    import numpy as np
from utilities.plotBucket import plotBucket
from utilities.plotBucket import plotBar
from utilities.plotBucket import plotFrequencyHistogram

df_paper = pd.read_pickle(
    "savedFrames/iteration5/paperTable")
df_review = pd.read_pickle(
    "savedFrames/iteration5/reviewTable")
df_industry = pd.read_pickle(
    "savedFrames/iteration5/industryReviewTable")
df_author = pd.read_pickle(
    "savedFrames/iteration5/authorTable")

#SECTION 1
#PAST PAPER COUNTS
df = df_paper  # [df_paper["paperCountPrimary"] > 0]
primary_different =\
    (df["paperCountPrimary"] != df["paperCountMax"])\
    | (df["paperCountMax"] == df["paperCount2ndHighest"])
df = df_paper
plotBucket(
    df,
    "paperCountAvg",
    "avgRating",
    numBuckets=5,
    color="green",
    x_label="Number of Past Papers",
    y_label="Average Rating",
    title="Rating vs. Average Past Paper Counts of Authors")
ylim([-1.8, 0])
p1 = plotBucket(
    df,
    "topPaperCountAvg",
    "avgRating",
    numBuckets=6,
    color="green",
    x_label="Number of Past Papers",
    y_label="Average Rating",
    title="Rating vs. Average Past Paper Counts of Authors")
p2 = plotBucket(
    df,
    "paperCountAvg",
    "avgRating",
    numBuckets=6,
    color="purple",
    sameFigure=True)
ylim([-2.0, 0])

legend([p1, p2], [
    "Avg Top Conference Papers",
    "Avg Past Papers"], loc=4)

p1 = plotBucket(
    df[primary_different],
    "paperCountMax",
    "avgRating",
    numBuckets=6,
    color="blue",
    x_label="Number of Past Papers",
    y_label="Average Rating",
    title="Rating vs. Past Paper Counts of Various Authors")

p2 = plotBucket(
    df[primary_different],
    "paperCountPrimary",
    "avgRating",
    numBuckets=6,
    color="red",
    sameFigure=True)
ylim([-1.8, 0])

legend([p1, p2], [
    "Most Experienced Author",
    "Primary Author"], loc=4)
p1 = plotBucket(
    df,
    "topPaperCountMax",
    "avgRating",
    numBuckets=6,
    color="blue",
    x_label="Number of Past Papers in Top Conferences",
    y_label="Average Rating",
    title="Rating vs. Top Past Paper Counts of Various Authors")
p2 = plotBucket(
    df,
    "topPaperCountPrimary",
    "avgRating",
    numBuckets=6,
    color="red",
    sameFigure=True)
ylim([-2.0, 0])

legend([p1, p2], [
    "Most Experienced Author",
    "Primary Author"], loc=4)

#Condition on Most Experienced Author
df = df[primary_different]

n = 2
breaks = [0, 100, 900]
paperCountMax = df["paperCountMax"]
slices =\
    [((paperCountMax > breaks[i]) & (paperCountMax <= breaks[i+1])) for i in range(n)]
slices[0] = ((paperCountMax >= breaks[0]) & (paperCountMax <= breaks[1]))
colors = ["#ff00ff", "#aa0000"]

p = []
for i in range(n):
    p.append(plotBucket(
        df[slices[i]],
        "paperCountPrimary",
        "avgRating",
        numBuckets=4,
        color=colors[i],
        x_label="Paper Count of Primary Author",
        y_label="Average Rating",
        title="Rating vs. Primary Author Paper Count Given Most Experienced",
        sameFigure=(i != 0),

        plotMean=True,
    ))
ylim([-1.8, 0])

legend(
    p,
    ["<= 100 Papers",
     "> 100 Papers"],
    loc=4,
    title="Most Experienced Author Paper Count",
    fontsize=12)

# Condition on Most Experienced Author
df = df_paper
df = df[df["topPaperCountPrimary"] != df["topPaperCountMax"]]

n = 2
breaks = [0, 40, 100]
paperCountMax = df["paperCountMax"]
slices =\
    [((paperCountMax > breaks[i]) & (paperCountMax <= breaks[i+1])) for i in range(n)]
slices[0] = ((paperCountMax >= breaks[0]) & (paperCountMax <= breaks[1]))
colors = ["#ff00ff", "#aa0000", "#00cc00"]

p = []
for i in range(n):
    p.append(plotBucket(
        df[slices[i]],
        "topPaperCountPrimary",
        "avgRating",
        numBuckets=10,
        color=colors[i],
        x_label="Top Paper Count of Primary Author",
        y_label="Average Rating",
        title="Rating vs. Primary Author Top Paper Count Given Most Experienced",
        sameFigure=(i != 0),
        plotMean=True,
        x_percentile=False
    ))
ylim([-1.5, 0])
xlim([0, 8])
legend(
    p,
    ["<= 50 Top Papers",
     "> 50 Top Papers"],
    loc=2,
    title="Most Experienced Author Top Paper Count",
    fontsize=12)

#SECTION 2
#Number of Authors
#Average Rating vs. Number of Authors given max count
df = df_paper
maxPaper = df["paperCountMax"]

n = 4
breaks = [0, 25, 100, 200, 900]
slices =\
    [((maxPaper >= breaks[i]) & (maxPaper <= breaks[i+1])) for i in range(n)]

p = plotBucket(
    df,
    "numAuthors",
    "avgRating",
    color="white",
    x_label="Number of Authors",
    y_label="Average Rating",
    marker="None",
    x_percentile=False
)
p = []
df1 = df.copy()[slices[0]]
ofInterest = df1["numAuthors"] >= 3
newValue = np.round(df1[ofInterest]["numAuthors"].mean(), 2)
df1.loc[ofInterest, "numAuthors"] = newValue
p.append(plotBar(
    df1,
    "numAuthors",
    "avgRating",
    [1, 2, newValue],
    color="blue",
    sameFigure=True,
    marker="s",
    plotMean=False))

colors = ["red", "green", "purple"]
p.extend([
    plotBucket(
        df[slices[i]],
        "numAuthors",
        "avgRating",
        numBuckets=4,
        color=colors[i-1],
        sameFigure=True,
            marker="s",
        plotMean=False)
    for i in [1,2,3]])

legend(
    p,
    ["Less than 25 Papers",
     "Between 25 and 100 Papers",
     "Between 100 and 200 Papers",
     "Greater than 200 Papers"],
    loc=4,
    title="Most Experienced Author Paper Count",
    fontsize=12)


p = plotBucket(
    df,
    "numAuthors",
    "avgRating",
    numBuckets=6,
    color="brown",
    x_label="Number of Authors",
    y_label="Average Rating",
    x_percentile=False
)
# #SECTION 3
#Status
df = pd.merge(
    df_paper,
    df_review, on=["paperId"])

df["statusMax"] =\
    df["paperCountReviewer"] - df["paperCountMax"]
df["statusPrimary"] =\
    df["paperCountReviewer"] - df["paperCountPrimary"]

#Status Plot 1
p1 = plotBucket(
    df,
    "statusMax",
    "rating",
    numBuckets=12,
    color="#ff5500",
    title="Average Rating vs. Status Difference between Reviewer and Author",
    x_label="Status Difference (Reviewer - Author)",
    y_label="Average Rating",
)
p2 = plotBucket(
    df,
    "statusPrimary",
    "rating",
    delta=10,
    color="#4422ff",
    sameFigure=True
)
plot(
    [0, 0],
    plt.ylim(),
    color='red',
    linewidth=.5,
    linestyle="--")
legend([p1, p2], ["Most Experienced Author", "Primary Author"], loc=3)

#Status plot conditional
simPercentiles = np.percentile(df["similarityMax"], [0, 33.3, 100])
colors = ["green", "blue", "purple"]

p = []
for i in range(2):
    df_curr = df[
        (df["similarityMax"] >= simPercentiles[i]) &
        (df["similarityMax"] <= simPercentiles[i+1])
    ]
    p.append(plotBucket(
        df_curr,
        "statusMax",
        "rating",
        numBuckets=10,
        color=colors[i],

        title="Avgerage Rating vs Status Difference\n"
        + "between Reviewer and Most Experienced Author",

        x_label="Status Difference (Reviewer - Author)",
        y_label="Average Rating",
            plotMean=False,
        sameFigure=(i != 0)
    ))
plot(
    [0, 0],
    plt.ylim(),
    color='red',
    linewidth=.5,
    linestyle="--")
legend(
    p,
    ["Low Similarity", "High Similarity"],
    loc=3)

#SECTION 4
#Co-Author Distance
df = df_review

#Distance Plot 1
p1 = plotBucket(
    df,
    "distAvg",
    "rating",
    numBuckets=7,
    x_label="Reviewer Author Distance",
    y_label="Avgerage Rating",
    xlim=[0, 8],
)
p2 = plotBar(
    df,
    "distMin",
    "rating",
    range(7)[1:],
    color="red",
    sameFigure=True,
)
legend([p1, p2],
       ["Average Author Distance",
       "Min Author Distances"])

#Distance Plot 2
plotBar(
    df,
    "distMin",
    "devPaperMean",
    range(7)[1:],
    x_label="Distance of Reviewer and Authors in Co-Authorship Graph",
    y_label="Deviation from Paper Average Rating",
    title="Deviation from Paper Average vs. Min Dist to Reviewer",
    color="Blue",
    xlim=[0, 7])

y = ylim()[1] - .05
for i in range(7)[1:]:
    text(i, y, df[df["distMin"] == i].shape[0], color="gray", ha="center")
text(3.5, y - .05, "(Number of Samples)", color="gray", ha="center")

##SECTION 5
df = df_paper
countryCounts = df['authorCountryMode'].value_counts().to_dict()
countries = [c for c, count in countryCounts.iteritems() if count > 10]
countries.sort(key=lambda c: df[df['authorCountryMode']==c]['accepted'].mean())

p = plotBar(
    df,
    "authorCountryMode",
    "accepted",
    countries,
    title="Proportion of Papers Accepted by Country",
    x_label="Mode Author Country",
    y_label="Proportion Accepted",
    categorical=True,
    errorBars = False
)

j = 0
for container in plt.gca().containers:
    for i, child in enumerate(container.get_children()):
        child.set_color(plt.cm.coolwarm_r((child.get_height() - 0.05)/0.20))
        j += 1
gcf().set_size_inches((40, 10))

y = ylim()[1] - 0.015
for i, country in enumerate(countries):
    submissions = countryCounts[country]
    accepted = df[(df['authorCountryMode'] == country) & df['accepted']].shape[0]
    text(i, y, r'$\frac{' + str(accepted) + '}{' + str(submissions) + '}$',
        color="black", ha="center", fontsize=16)

text(
    len(countries)/2.0 - .5,
    y - 0.015,
    "(Number Accepted / Number Submitted)",
    color="gray", ha="center")


#Review Length Plots
df = pd.merge(df_paper, df_review, on="paperId")

#Plot 1 -- Reviewer Length by Reviewer Country
reviewerCounts = df[["userId", "countryReviewer"]]\
    .drop_duplicates()["countryReviewer"]\
    .value_counts().to_dict()

countries = [c for c, count in reviewerCounts.iteritems() if count > 3]
countries.sort(key=lambda c: df[df["countryReviewer"]==c]["reviewLength"].mean())

p = plotBar(
    df,
    "countryReviewer",
    "reviewLength",
    countries,
    title="Review Length by Reviewer Country",
    x_label="Reviewer Country",
    y_label="Average Review Length",
    categorical=True
)

j = 0
for container in plt.gca().containers:
    for i, child in enumerate(container.get_children()):
        if j > 3:
            child.set_color(plt.cm.coolwarm_r((child.get_height() - 250)/120.0))
        j += 1
gcf().set_size_inches((40, 10))

y = ylim()[1] - 10
for i, country in enumerate(countries):
    text(i, y, reviewerCounts[country], color="gray", ha="center")

text(
    len(countries)/2.0 - .5,
    y - 10,
    "(Number of Reviewers)",
    color="gray", ha="center")


#Plot 1.5 == Reviewer Accuracy by Reviewer Country
reviewerCounts = df[["userId", "countryReviewer"]]\
    .drop_duplicates()["countryReviewer"]\
    .value_counts().to_dict()

df["reviewerInfluence"] = (df["rating"] > 0) == (df["accepted"])

countries = [c for c, count in reviewerCounts.iteritems() if count > 3]
countries.sort(key=lambda c: df[df["countryReviewer"]==c]["reviewerInfluence"].mean())

p = plotBar(
    df,
    "countryReviewer",
    "reviewerInfluence",
    countries,
    title="Reviewer Accuracy by Reviewer Country",
    x_label="Reviewer Country",
    y_label="Proportion of Ratings that Agree with Decision",
    categorical=True
)

j = 0
for container in plt.gca().containers:
    for i, child in enumerate(container.get_children()):
        if j > 3:
            child.set_color(plt.cm.coolwarm_r((child.get_height() - 0.709)/0.2))
        j += 1
gcf().set_size_inches((40, 10))

y = ylim()[1] - 0.05
for i, country in enumerate(countries):
    text(i, y, reviewerCounts[country], color="gray", ha="center")

text(
    len(countries)/2.0 - .5,
    y - 0.05,
    "(Number of Reviewers)",
    color="gray", ha="center")

#Plot 2 -- Review Length and Rating Magnitude
df["absrating"] = df["rating"].abs()
plotBucket(
    df,
    "reviewLength",
    "absrating",
    numBuckets=8,
    x_percentile=False,
    xlim=[0, 600],
    x_label="Review Length (words)",
    y_label="Rating Magnitude (Absolute Value)",
    title="Rating Magnitude vs. Review Length")
ylim([1, 2.2])
plot(
    [df["reviewLength"].median()] * 2,
    plt.ylim(),
    color='red',
    linewidth=1,
    linestyle="--")

#Plot 3 -- Review Length and Influence
df["agreement"] = (df["rating"] > 0) == df["accepted"]

n = 4
bins = np.percentile(df["reviewLength"].values, list(np.linspace(0, 100, n+1)))
slices = [
    (df["reviewLength"] > bins[i])
    & (df["reviewLength"] <= bins[i+1])
    for i in range(n)
]

values = [
    df[slices[i]]["agreement"].mean()
    for i in range(n)
]

yerr = [
    math.sqrt(values[i]*(1-values[i])*1.0/df[slices[i]].shape[0])
    for i in range(n)
]

figure(facecolor="white")
bar(range(n), values, yerr=yerr, ecolor="black", color="#80a0ff")
ylim([.7, .85])
xlim([-.2, n])
xticks(np.arange(0, n) + .5,
       ["0-25%", "25-50%", "50-75%", "75-100%"])
xlabel("Review Length (Percentile Scale)")
ylabel("Proportion of Reviews that Agree with Acceptance")
plt.suptitle("Review Influence")

##SECTION 6
#Review Time
df = pd.merge(df_review, df_paper, on="paperId")
df['time'] = df['time'].values.astype(datetime.datetime)


def transformDates(dateLabels):
    return list(pd.Series([
        datetime.datetime.strptime(d + '/2014', '%m/%d/%Y')
        for d in dateLabels
    ]).values.astype(datetime.datetime))


def plotDeadline(yoffset=10):
    deadline = '4/15'
    plot(
        transformDates([deadline]) * 2,
        ylim(),
        color="red",
        linestyle="--",
        linewidth=2,
        alpha=.8)
    text(
        transformDates([deadline])[0],
        ylim()[1] - yoffset,
        "  Review Submission\n  Deadline",
        va="top",
        color="red",
        alpha=.8)


labels_month = ['3/20', '3/30', '4/10', '4/20', '4/30']
dates_month = transformDates(labels_month)

#Plot 1 -- Submissions in last 5 days
labels_5Days = [
    '4/10',
    '4/11',
    '4/12',
    '4/13',
    '4/14',
    '4/15',
    '4/16',
    '4/17',
]
dates_5Days = transformDates(labels_5Days)
datesMidDay = [.5*(dates_5Days[i] + dates_5Days[i+1])
               for i in range(len(dates_5Days) - 1)]

plotFrequencyHistogram(
    df,
    'time',
    'Submission Date',
    myBins=dates_5Days,
    plotMean=False
)
xticks(datesMidDay, labels_5Days[:-1])
plotDeadline()

#Plot 2 -- Submissions in the last 12 hours
labels_12Hours = [
    '4/14 12:00 PM',
    '4/14 2:00 PM',
    '4/14 4:00 AM',
    '4/14 6:00 PM',
    '4/14 8:00 PM',
    '4/14 10:00 PM',
    '4/15 12:00 AM',
    '4/15 2:00 AM',
]

dates_12Hours = []
for h in range(6):
    dates_12Hours.append(
        datetime.datetime(2014, 4, 14, h*2+12)
    )
for h in range(2):
    dates_12Hours.append(
        datetime.datetime(2014, 4, 15, h*2)
    )
dates_12Hours = list(pd.Series(dates_12Hours).values.astype(datetime.datetime))

plotFrequencyHistogram(
    df,
    'time',
    'Submission Time',
    myBins=dates_12Hours,
    plotMean=False
)
xticks(dates_12Hours, labels_12Hours)
plotDeadline()


#Plot 3 -- Submission Time vs. Rating
plotBucket(
    df,
    'time',
    'rating',
    numBuckets=5,
    x_percentile=False,
    title='Rating v. Submission Date',
    x_label="Submission Date",
    y_label="Average Review Rating",
)
xticks(dates_month, labels_month)
#xticks(dates_5Days, labels_5Days)
#xlim([dates_5Days[0], dates_5Days[-1]])
plotDeadline(.1)

#Plot 4 -- Submission Time vs. P(Positive)
df["positive"] = df["rating"] > 0
plotBucket(
    df,
    'time',
    'positive',
    numBuckets=5,
    x_percentile=False,
    title='Positive Ratings v. Submission Date',
    x_label="Submission Date",
    y_label="Proportion of Ratings that were Positive",
)
xticks(dates_month, labels_month)
plotDeadline(.1)

#Plot 5 -- Submission Time vs. Magnitude
df["absRating"] = df["rating"].abs()
plotBucket(
    df,
    'time',
    'absRating',
    numBuckets=7,
    x_percentile=False,
    title='Rating Magnitude v. Submission Date',
    x_label="Submission Date",
    y_label="Rating Magnitude",
)
xticks(dates_month, labels_month)
plotDeadline(.1)

#Plot 6 -- Submission Time vs. Each Rating
ratingDict = {
    -3: "Strong Reject",
    -2: "Reject",
    -1: "Weak Reject",
    1: "Weak Accept",
    2: "Accept",
    3: "Strong Accept",
}

legendLabels = [
    "Reject & Strong Reject",
    "Weak Reject",
    "Weak Accept",
    "Accept & Strong Accept"
]

colors = ["red", "", "orange", "",  "blue", "green"]
p = []
for r in [[-2, -3], [-1], [1], [2, 3]]:
    df["currRating"] = df["rating"].isin(r)
    p.append(plotBucket(
        df,
        'time',
        'currRating',
        numBuckets=6 if len(r) == 1 else 5,
        color=colors[min(r)+3],
        x_percentile=False,
        title='Rating Type v. Submission Date',
        x_label="Submission Date",
        y_label="Proportion of Ratings",
        sameFigure=(min(r) != -3),
        plotMean=False
    ))
xticks(dates_month, labels_month)
xlim(transformDates(["4/7", "4/23"]))
plotDeadline(.05)
ylim([-0.1, 0.5])
legend(p, legendLabels, loc=4)

#Plot 7 -- Submission Time vs. Influence
df["agree"] = (df["rating"] > 0) == df["accepted"]
plotBucket(
    df,
    'time',
    'agree',
    numBuckets=10,
    x_percentile=False,
    title='Review Influence v. Submission Date',
    x_label="Submission Date",
    y_label="Proportion of Reviews that Agree with Outcome",
)
ylim([.7, .9])

labels = ["4/%d" % d for d in np.arange(13, 20)]
xticks(transformDates(labels), labels)
xlim(transformDates(["4/12", "4/19"]))
plotDeadline(.05)


#Plot 8 -- Submission Time vs. Review Length
plotBucket(
    df,
    'time',
    'reviewLength',
    numBuckets=10,
    x_percentile=False,
    title='Review Length v. Submission Date',
    x_label="Submission Date",
    y_label="Review Length (words)",
)

#labels = ["4/6", "4/10", "4/14", "4/16", "4/18"]
#xticks(transformDates(labels), labels)
#xlim(transformDates(["4/5", "4/20"]))

xticks(dates_5Days[1:], labels_5Days[1:])
xlim([dates_5Days[0], dates_5Days[-1]])
plotDeadline()

##SECTION 7
#Industry vs. Research

#Plot 1 -- Histogram of Ratings
plotFrequencyHistogram(
    df_industry,
    "rating",
    "Industry Paper Ratings",
    color="#B9E84D",
    myBins=[-2.4, -1.2, 0, 1.2, 2.4],
    plotMean=False)
xticks([-1.8, -.6, .6, 1.8],
       ["Reject", "Weak Reject",
        "Weak Accept", "Accept"])
colors =\
    ["#FF5C54", "#FFA6A1", "#A1D3FF", "#54B2FF"]
for container in plt.gca().containers:
    for i, child in enumerate(container.get_children()):
        child.set_color(colors[i])

#Plots 2-4 -- Bar Plot Comparisons


def plotComparison(col, label):
    industry = df_industry[col]
    research = df_review[col]

    x = [0, 1]
    y = [industry.mean(), research.mean()]
    yerr = (
        industry.std()/math.sqrt(industry.shape[0]),
        research.std()/math.sqrt(research.shape[0]))

    plt.figure(facecolor="white")
    gca().bar(x, y, yerr=yerr, ecolor="black")
    ylabel(label)

    xticks([.4, 1.4], ["Industry Track", "Research Track"])
    xlim([-.2, 2])
    plt.suptitle("Comparing "+label)

    j = 0
    colors = ["#E3CBFF", "#C7FFB9"]
    for container in plt.gca().containers:
        for i, child in enumerate(container.get_children()):
            if j > 3:
                child.set_color(colors[i])
            j += 1

plotComparison("rating", "Average Rating")
plotComparison("reviewLength", "Review Length")

df_industry["devPaperMeanAbs"] = df_industry["devPaperMean"].abs()
df_review["devPaperMeanAbs"] = df_review["devPaperMean"].abs()
plotComparison("devPaperMeanAbs", "Average Deviation from Paper Mean")

#Plot 5 -- Submission Time Near Deadline

df_industry['time'] =\
    df_industry['time'].values.astype(datetime.datetime)

plotFrequencyHistogram(
    df_industry,
    'time',
    'Submission Date',
    myBins=dates_5Days,
    color="#E3CBFF",
    plotMean=False
)
xticks(dates_5Days, labels_5Days)
plotDeadline()

##SECTION 8
#Affiliations
df = df_author

cutoff = 20
counts = df["affiliation"].value_counts()
affiliations = counts[counts >= cutoff].index.tolist()
rates = df.groupby("affiliation")["acceptanceRate"].mean()

affiliations.sort(key=lambda a: rates[a])


p = plotBar(
    df,
    "affiliation",
    "acceptanceRate",
    affiliations,
    title="Acceptance Rate by Affiliation",
    x_label="Author Affiliation",
    y_label="Acceptance Rate",
    categorical=True,
    horizontal=True
)

affiliationText = {
    "Stanford University": "Stanford",
    "Arizona State University": "ASU",
    "Hong Kong University of Science and Technology": "Hong Kong\n(HKUST)",
    "Carnegie Mellon University": "CMU",
    "Georgia Institute of Technology": "Georgia Tech",
    "University of Technology Sydney": "U of Tech\nSydney",
    "Nanyang Technological University": "Nanyang Tech",
    "Chinese Academy of Sciences": "Chinese\nAcad. of Sci",
    "SUNY Buffalo": "SUNY\nBuffalo",
}

labels = [
    affiliationText[a] if a in affiliationText else a
    for a in affiliations]
labels = [
    l.replace(" University", "").replace("University of ", "")
    for l in labels]
yticks(range(len(affiliations)), labels, fontsize=10)

j = 0
for container in plt.gca().containers:
    for i, child in enumerate(container.get_children()):
        if j > 3:
            child.set_color(
                plt.cm.coolwarm_r(
                    child.get_width()/max(rates[affiliations])))
        j += 1

x = xlim()[1] - .03
for i, a in enumerate(affiliations):
    text(x, i, counts[a], color="gray", va="center")

text(
    x - .02,
    len(affiliations)/2.0 - .5,
    "(Number of Authors)",
    color="gray", va="center",
    rotation="vertical")


##SECTION 9
#Subject Area
df = df_paper
subjArea = "subjectAreaPrimaryGeneral"

cutoff = 50
counts = df[subjArea].value_counts()
areas = counts[counts >= cutoff].index.tolist()
rates = df.groupby(subjArea)["accepted"].mean()

areas.sort(key=lambda a: rates[a])


p = plotBar(
    df,
    subjArea,
    "accepted",
    areas,
    title="Acceptance Rate by Subject Area",
    x_label="Subject Area",
    y_label="Acceptance Rate",
    categorical=True
)

j = 0
for container in plt.gca().containers:
    for i, child in enumerate(container.get_children()):
        if j > 3:
            child.set_color(
                plt.cm.coolwarm_r(
                    (child.get_height() - .1)/.1))
        j += 1

y = ylim()[1] - .01
for i, a in enumerate(areas):
    text(i, y, counts[a], color="gray", ha="center")

text(
    len(areas)/2.0 - .5,
    y - .015,
    "(Number of Papers)",
    color="gray", ha="center")

##SECTION 10
#Review Text Classifier
df = df_paper[df_paper["accuracyReviewText"] > -1]

plotBar(
    df,
    "accepted",
    "accuracyReviewText",
    [False, True],
    categorical=True,
    x_label="Acceptance of Paper",
    y_label="Classifier (1) Accuracy",
    title="Classification Accuracy vs. Paper Acceptance",
    color="#E49CFF"
)

plotBucket(
    df,
    "topPaperCountMax",
    "accuracyReviewText",
    numBuckets=5,
    title="Classifier Accuracy for Most Experienced Author",
    x_label="Top Paper Count of Most Experienced Author",
    y_label="Classifier (1) Accuracy"
)


df = pd.merge(df_review, df_paper, on="paperId")

plotBucket(
    df,
    "paperCountReviewer",
    "accuracyRating",
    title="Classifier Accuracy by Reviewer Experience",
    x_label="Paper Count of Reviewer",
    y_label="Classifier (3) Accuracy",
    numBuckets=5,
)
ylim([.7, 1])

plotBar(
    df,
    "rating",
    "accuracyRating",
    [-3, -2, -1, 1, 2, 3],
    categorical=True,
    x_label="Rating",
    y_label="Classifier (3) Accuracy",
    title="Classifier Accuracy by Rating",
    color="#E8A482"
)

plotBar(
    df,
    "rating",
    "accuracyAcceptance",
    [-3, -2, -1, 1, 2, 3],
    categorical=True,
    x_label="Rating",
    y_label="Classifier (2) Accuracy",
    title="Classifier Accuracy by Rating",
    color="#FFF9A2"
)

df['time'] = df['time'].values.astype(datetime.datetime)
plotBucket(
    df,
    "time",
    "accuracyAcceptance",
    numBuckets=8,
    x_percentile=False,
    x_label="Submission Date",
    y_label="Accuracy of Predicting Review Rating",
    title="Classifier Accuracy vs. Submission Date"
)
ylim([.65, .85])

plotDeadline(.03)
xticks(dates_month, labels_month)

plotBucket(
    df,
    "reviewLength",
    "accuracyRating",
    x_label="Review Length",
    y_label="Classifier (3) Accuracy",
    title="Classifier Accuracy vs. Review Length",
    numBuckets=5,
)
ylim([.8, .9])


df['accurateRating'] = df['accuracyRating'] > .5
plotBar(
    df,
    "accurateRating",
    "reviewLength",
    [False, True],
    categorical=True,
    x_label="Classifier (3) was Accurate",
    y_label="Review Length",
    title="Review Length vs. Classification Accuracy",
    color="#FF7D79"
)

df['influenceProxy'] = (df['rating'] > 0) == df['accepted']
df['accurateAcceptance'] = df['accuracyAcceptance'] > .5

plotBar(
    df,
    "accurateAcceptance",
    "influenceProxy",
    [False, True],
    categorical=True,
    x_label="Classifier (2) was Accurate",
    y_label="P(Agree)",
    title="Influence vs. Classification Accuracy",
    color="#A3FF8F"
)

plotBar(
    df,
    "influenceProxy",
    "accuracyAcceptance",
    [False, True],
    categorical=True,
    y_label="Classifier (2) Accuracy",
    x_label="Agree with Acceptance",
    title="Classification Accuracy vs. Influence",
    color="#82C8E8"
)

##SECTION (2)a
#Connectivity
p1 = plotBucket(
    df,
    "connectivity",
    "avgRating",
    numBuckets=7,
    x_label="Measure of Connectivity",
    y_label="Average Rating",
    title="Rating vs. Connectivity of Authors in Co-Author Graph",
)

p2 = plotBucket(
    df,
    "degreeCentrality",
    "avgRating",
    numBuckets=5,
    color="red",
    sameFigure=True
)

legend(
    [p2, p1],
    ["Degree Centrality", "Number of 2nd Degree Connections"],
    loc=4)

show()
