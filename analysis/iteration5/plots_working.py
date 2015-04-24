import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
    import numpy as np
from utilities.plotBucket import plotBucket
from utilities.plotBucket import plotBar
from utilities.plotBucket import plotFrequencyHistogram
from utilities.plotBucket import setUpPlot

df_paper = pd.read_pickle(
    "savedFrames/iteration5/paperTable")
df_review = pd.read_pickle(
    "savedFrames/iteration5/reviewTable")
df_industry = pd.read_pickle(
    "savedFrames/iteration5/industryReviewTable")
df_author = pd.read_pickle(
    "savedFrames/iteration5/authorTable")


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

labels_month = ['3/20', '3/30', '4/10', '4/20', '4/30']
dates_month = transformDates(labels_month)

####################################################




df = pd.merge(df_paper, df_review, on="paperId")
df = df_paper
# df["agreement"] = (df["rating"] > 0) == df["accepted"]
# plotBar(
#     df,
#     "rating",
#     "agreement",
#     [-3, -2, -1, 1, 2, 3],
#     x_label="Review Rating",
#     y_label="Proportion of Reviews that Agree with Acceptance",
#     title="Review Influence by Rating",
#     categorical=True)
# xticks(range(6),
#        ["Strong Reject", "Reject", "Weak Reject",
#        "Weak Accept", "Accept", "Strong Accept"])

# colors =\
#     ["#FF1C00", "#FF5C54", "#FFA6A1", "#A1D3FF", "#54B2FF", "#006FFF"]
# j = 0
# for container in plt.gca().containers:
#     for i, child in enumerate(container.get_children()):
#         if j > 3:
#             child.set_color(colors[i])
#         j += 1

# ylim([0, 1.08])
# counts = df["rating"].value_counts()
# y = ylim()[1] - .05
# for i, a in enumerate([-3, -2, -1, 1, 2, 3]):
#     text(i, y, counts[a], color="gray", ha="center")

# text(
#     6/2.0 - .5,
#     y - .04,
#     "(Count of Rating)",
#     color="gray", ha="center")

# df["agreement"] = (df["rating"] > 0) == df["accepted"]

# n = 4
# bins = np.percentile(df["reviewLength"].values, list(np.linspace(0, 100, n+1)))
# slices = [
#     (df["reviewLength"] > bins[i])
#     & (df["reviewLength"] <= bins[i+1])
#     for i in range(n)
# ]

# values = [
#     df[slices[i]]["agreement"].mean()
#     for i in range(n)
# ]

# yerr = [
#     math.sqrt(values[i]*(1-values[i])*1.0/df[slices[i]].shape[0])
#     for i in range(n)
# ]

# figure(facecolor="white")
# bar(range(n), values, yerr=yerr, ecolor="black", color="#80a0ff")
# ylim([.7, .85])
# xlim([-.2, n])
# xticks(np.arange(0, n) + .5,
#        ["0-25%", "25-50%", "50-75%", "75-100%"])
# xlabel("Review Length (Percentile Scale)")
# ylabel("Proportion of Reviews that Agree with Acceptance")

# df.loc[df["authorCountryMode"] == "United Kingdom", "authorCountryMode"]\
#     = "United\nKingdom"
# df.loc[df["authorCountryMode"] == "South Korea", "authorCountryMode"]\
#     = "South\nKorea"
# countryCounts = df['authorCountryMode'].value_counts().to_dict()
# countries = [c for c, count in countryCounts.iteritems() if count > 10]
# countries.sort(key=lambda c: countryCounts[c])
# df["countryCount"] = 0
# for c in countries:
#     df.loc[df["authorCountryMode"] == c, "countryCount"] = countryCounts[c]

# p = plotBar(
#     df,
#     "authorCountryMode",
#     "countryCount",
#     countries,
#     x_label="Mode Author Country",
#     y_label="Number of Submissions",
#     categorical=True,
#     errorBars=False,
#     plotMean=False
# )

# j = 0
# for container in plt.gca().containers:
#     for i, child in enumerate(container.get_children()):
#         child.set_color(plt.cm.coolwarm_r((child.get_height())/250.0))
#         j += 1
# gcf().set_size_inches((40, 10))

# y = ylim()[1] - 20
# for i, country in enumerate(countries):
#     submissions = countryCounts[country]
#     text(i, y, r'$' + str(submissions) + '$',
#          color="black", ha="center", fontsize=16)



df.loc[df["authorCountryMode"] == "United Kingdom", "authorCountryMode"]\
    = "United\nKingdom"
countryCounts = df['authorCountryMode'].value_counts().to_dict()
countries = [c for c, count in countryCounts.iteritems() if count > 10]
countries.sort(key=lambda c: df[df['authorCountryMode']==c]['accepted'].mean())
countries = countries[1:]

p = plotBar(
    df,
    "authorCountryMode",
    "accepted",
    countries,
    title="Proportion of Papers Accepted by Country",
    x_label="Mode Author Country",
    y_label="Proportion Accepted",
    categorical=True,
    errorBars=True
)

j = 0
for container in plt.gca().containers:
    for i, child in enumerate(container.get_children()):
        if j > 3:
            child.set_color(plt.cm.coolwarm_r((child.get_height() - 0.05)/0.20))
        j += 1
gcf().set_size_inches((40, 10))

y = ylim()[1] - 0.025
for i, country in enumerate(countries):
    submissions = countryCounts[country]
    accepted = df[(df['authorCountryMode'] == country) & df['accepted']].shape[0]
    text(i, y, r'$\frac{' + str(accepted) + '}{' + str(submissions) + '}$',
         color="black", ha="center", fontsize=16)

text(
    len(countries)/2.0 - .5,
    y - 0.025,
    "(Number Accepted / Number Submitted)",
    color="gray", ha="center")


# subjArea = "subjectAreaPrimaryGeneral"

# cutoff = 50
# counts = df[subjArea].value_counts()
# areas = counts[counts >= cutoff].index.tolist()
# rates = df.groupby(subjArea)["accepted"].mean()

# areas.sort(key=lambda a: rates[a])


# p = plotBar(
#     df,
#     subjArea,
#     "accepted",
#     areas,
#     title="Acceptance Rate by Subject Area",
#     x_label="Subject Area",
#     y_label="Acceptance Rate",
#     categorical=True
# )
# xticks(range(8), [
#     "Graph\nmining",
#     "Mining rich\ndata types",
#     "Social",
#     "Recommender\nSystems",
#     "Unsupervised\nLearning",
#     "Applications",
#     "Supervised\nLearning",
#     "Big Data"
# ])

# j = 0
# for container in plt.gca().containers:
#     for i, child in enumerate(container.get_children()):
#         if j > 3:
#             child.set_color(
#                 plt.cm.coolwarm_r(
#                     (child.get_height() - .1)/.1))
#         j += 1

# y = ylim()[1] - .01
# for i, a in enumerate(areas):
#     text(i, y, counts[a], color="gray", ha="center")

# text(
#     len(areas)/2.0 - .5,
#     y - .015,
#     "(Number of Papers)",
#     color="gray", ha="center")
















# plotBucket(
#     df,
#     "abstractLength",
#     "accuracyAbstract",
#     x_percentile=False,
#     numBuckets=5,
#     x_label="Abstract Length (Words)",
#     y_label="Classification Accuracy",
#     title="Classification Accuracy vs. Abstract Length"
# )

# plotBucket(
#     df,
#     "avgRating",
#     "accuracyAbstract",
#     x_percentile=False,
#     numBuckets=8,
#     x_label="Average Rating",
#     y_label="Classification Accuracy",
#     title="Classification Accuracy vs. Paper Rating"
# )
# xlim([-3, 2])

# plotBucket(
#     df,
#     "topPaperCountMax",
#     "accuracyAbstract",
#     x_label="Top Paper Count of Most Experienced Author",
#     y_label="Classification Accuracy",
#     title="Classification Accuracy by Author Experience",
#     numBuckets=5
# )

# p1 = plotBucket(
#     df,
#     "connectivity",
#     "avgRating",
#     numBuckets=7,
#     x_label="Measure of Connectivity",
#     y_label="Average Rating",
#     title="Rating vs. Connectivity of Authors in Co-Author Graph",
# )

# p2 = plotBucket(
#     df,
#     "degreeCentrality",
#     "avgRating",
#     numBuckets=5,
#     color="red",
#     sameFigure=True
# )

# legend(
#     [p2, p1],
#     ["Degree Centrality", "Number of 2nd Degree Connections"],
#     loc=4)

# df.loc[df["numAuthors"] > 7, "numAuthors"] = 7
# p = plotBar(
#     df,
#     "numAuthors",
#     "avgRating",
#     range(8),
#     color="green",
#     x_label="Number of Authors",
#     y_label="Average Rating",
#     xlim=[0, 8],
# )
# xticks(range(8)[1:], [1, 2, 3, 4, 5, 6, "7+"])


# df = pd.merge(df_review, df_paper, on="paperId")
# df['time'] = df['time'].values.astype(datetime.datetime)

# labels_5Days = [
#     '4/10',
#     '4/11',
#     '4/12',
#     '4/13',
#     '4/14',
#     '4/15',
#     '4/16',
#     '4/17',
# ]
# dates_5Days = transformDates(labels_5Days)

# plotFrequencyHistogram(
#     df,
#     'time',
#     'Submission Date',
#     myBins=dates_5Days,
#     plotMean=False,
#     color="#D6FFD8"
# )

# xticks(dates_5Days, labels_5Days)
# plotDeadline()

show()
