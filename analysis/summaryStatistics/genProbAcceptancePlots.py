import warnings
import matplotlib as mpl
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from pandas import DataFrame, Series
    import pandas as pd
from utilities.plotBucket import plotBar

acceptanceRate = 152.0/998.0

options = {}
options["errorBars"] = True


papersFrame = pd.read_pickle(
    "savedFrames/summaryStatistics/papersTable")
userFrame = pd.read_pickle(
    "savedFrames/summaryStatistics/userTable")


def getAcceptedTable(frame, col1, col2):
    df = frame\
        .groupby(col1)[col2]\
        .value_counts()\
        .unstack().fillna(0)
    df["total"] = df.sum(axis=1)
    df["probability"] = df[1] / df["total"]
    df["error"] = df["probability"]*(1-df["probability"])/sqrt(df["total"])
    return df


def getErrorBars(totals, prob):
    error = np.sqrt((prob * (1-prob))/totals)
    return [error, error]


def getProbabilityAxis(size, ishorizontal):
    fig = plt.figure(figsize=size)
    ax = fig.add_subplot(111)
    fig.set_facecolor("white")

    if ishorizontal:
        settingsHorizontal(ax)
    else:
        settingsVertical(ax)

    return ax


def settingsHorizontal(ax):
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.yaxis.grid(False)
    ax.xaxis.tick_top()
    plt.subplots_adjust(top=.9, bottom=.05)
    ax.title.set_position((.5, 1.05))


def settingsVertical(ax):
    pass


def interpolateColor(dataSeries, ax, colorMap):
    cmin, cmax = .2, 1
    xmin, xmax = min(dataSeries), max(dataSeries)

    cmin = 0.2
    cmax = .9
    xmin = 0.0
    xmax = 100.0

    interpolate = lambda x: cmin + (cmax - cmin)*(x - xmin)/(xmax - xmin)
    colors = [interpolate(min([x, 100])) for x in dataSeries]

    for container in ax.containers:
        for i, child in enumerate(container.get_children()):
            child.set_color(colorMap(colors[i]))


def plotProbabilityHistogram(show, frame, title, xlab, colormap, startBins=0):
    if show:
        acceptValues = getValues(1, frame)
        rejectValues = getValues(0, frame)
        totalValues = acceptValues + rejectValues

        if (startBins > 0):
            acceptHist, bins = np.histogram(acceptValues, startBins)
        else:
            acceptHist, bins = np.histogram(acceptValues)
        totalHist, bins_na = np.histogram(totalValues, bins)

        probHist = acceptHist*1.0/totalHist
        ax = getProbabilityAxis((10, 10), False)

        width = (bins[1] - bins[0])*.95
        center = (bins[:-1] + bins[1:])/2
        if options["errorBars"]:
            ax.bar(
                center,
                probHist,
                align='center',
                width=width,
                color=colormap(50),
                yerr=getErrorBars(totalHist, probHist),
                error_kw=dict(ecolor='black', lw=2, capsize=5, capthick=2))
        else:
            ax.bar(
                center,
                probHist,
                align='center',
                width=width)

            interpolateColor(totalHist, ax, colormap)

        ax.set_title(title)
        xlabel(xlab)
        ylabel("Probability of Acceptance")

        #plot average line
        plot(
            [0, bins[-1]],
            [acceptanceRate, acceptanceRate],
            color='black',
            linewidth=2.5,
            linestyle="--")

        return ax


def getValues(x, frame):
    a = frame[x].to_dict()
    a = [[k] * v for k, v in a.iteritems()]
    return [i for j in a for i in j]

def addNoise(series, stddev):
    return series + stddev*np.random.randn(len(series))


####PLOTS


def plotSubjectArea():
    subjectArea = getAcceptedTable(
        papersFrame,
        "primarySubjectArea",
        "accepted")

    # #PLOT 1
    # subjectArea["probability"].plot(
    #     kind="barh",
    #     xerr=getErrorBars(subjectArea["error"]),
    #     colormap="winter",
    #     legend=False)

    #PLOT 2
    subjectArea = subjectArea.sort("probability")
    ax = getProbabilityAxis((30, 10), True)
    subjectArea[["probability"]].plot(
        kind="barh",
        ax=ax,
        legend=False,
        title="Probability of Acceptance For Subject Area")
    ylabel("Primary Subject Area")
    interpolateColor(subjectArea["total"], ax, mpl.cm.Blues)

#plotSubjectArea()

#Number of Bids
bids = getAcceptedTable(papersFrame, "#Bids", "accepted")
plotProbabilityHistogram(
    True,
    bids,
    "Probability vs. Number of Bids",
    "Number of Bids",
    mpl.cm.Greens)

#Number of Authors
authors = getAcceptedTable(papersFrame, "#Authors", "accepted")
plotProbabilityHistogram(
    True,
    authors,
    "Probability vs. Number of Authors",
    "Number of Authors",
    mpl.cm.Reds,
    range(0, 10, 1))

#Number of Papers Submitted
papersSubmitted = getAcceptedTable(userFrame, "#Papers", "hasAcceptedPaper")
plotProbabilityHistogram(
    True,
    papersSubmitted,
    "Prob. of getting at least one paper accepted vs. Number of Submissions",
    "Number of Submissions",
    mpl.cm.PuRd,
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

#Number of Past Papers Papers
pastPapers = getAcceptedTable(userFrame, "#PastPapers", "hasAcceptedPaper")
plotProbabilityHistogram(
    True,
    pastPapers,
    "Prob. of getting at least one paper accepted vs. Number of Past Papers",
    "Number of Past Papers",
    mpl.cm.Oranges,
    [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120])

#Average Overall Rating
avgRating = getAcceptedTable(papersFrame, "avgRating", "accepted")
plotProbabilityHistogram(
    True,
    avgRating,
    "Probability vs. Average Rating",
    "Average Rating",
    mpl.cm.OrRd)

#Variance in Overall Ratings (At least 3 ratings)
varRating = getAcceptedTable(papersFrame, "varRating", "accepted")
plotProbabilityHistogram(
    True,
    varRating,
    "Probability vs. Variance in Rating",
    "Variance in Rating",
    mpl.cm.BuGn,
    [0, 1, 2, 3, 4])


#average rating vs variance
# ax = getProbabilityAxis((10, 10), False)
# plt.scatter(
#     addNoise(papersFrame[papersFrame["accepted"] == 1]["avgRating"], .2),
#     addNoise(papersFrame[papersFrame["accepted"] == 1]["varRating"], .2), c="Red")
# plt.scatter(
#     addNoise(papersFrame[papersFrame["accepted"] == 0]["avgRating"], .2),
#     addNoise(papersFrame[papersFrame["accepted"] == 0]["varRating"], .2), c="Blue")
# xlabel("Average Rating")
# ylabel("Rating Variance")

#sum of past paper counts
sumPastPapers = getAcceptedTable(papersFrame, "authorsPastPaperCount", "accepted")
plotProbabilityHistogram(
    True,
    sumPastPapers,
    "Prob. of Acceptance vs. Sum of Authors' Past Paper Counts",
    "Past Paper counts",
    mpl.cm.YlOrRd)

plotProbabilityHistogram(
    True,
    sumPastPapers,
    "Prob. of Acceptance vs. Sum of Authors' Past Paper Counts",
    "Past Paper counts",
    mpl.cm.YlOrRd,
    range(0, 600, 40))

#max of author's past paper counts
maxPastPapers = getAcceptedTable(papersFrame, "authorsMaxPastPaper", "accepted")
plotProbabilityHistogram(
    True,
    maxPastPapers,
    "Prob. of Acceptance vs. Max of Authors' Past Paper Counts",
    "Past Paper counts",
    mpl.cm.YlGn)

plotProbabilityHistogram(
    True,
    maxPastPapers,
    "Prob. of Acceptance vs. Max of Authors' Past Paper Counts",
    "Past Paper counts",
    mpl.cm.YlGn,
    range(0, 440, 40))

show()
