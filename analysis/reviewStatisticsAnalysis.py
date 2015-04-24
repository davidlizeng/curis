import warnings
import matplotlib as mpl
import numpy as np
import math
from pylab import *
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from utilities.plotBucket import plotBucket
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from pandas import DataFrame, Series
    import pandas as pd

reviewFrame = pd.read_pickle(
    "savedFrames/reviewStatistics/reviewTable")
metaReviewFrame = pd.read_pickle(
    "savedFrames/reviewStatistics/metaReviewTable")
bidFrame = pd.read_pickle(
    "savedFrames/reviewStatistics/bidTable")
paperFrame = pd.read_pickle(
    "savedFrames/reviewStatistics/paperTable")
userFrame = pd.read_pickle(
    "savedFrames/reviewStatistics/userTable")





reviewsWithBids = reviewFrame.merge(bidFrame, how='left', on=['userId', 'paperId']).fillna(0)
reviewsWithHistory = reviewFrame.merge(userFrame, how='left', on='userId').merge(paperFrame, how='left', on='paperId')

meansMin = []
stdDevsMin = []
numsMin = []
stdErrorsMin = []
for i in range(1, 8):
    meansMin.append(reviewFrame[reviewFrame['minDist'] == i]['rating'].mean())
    stdDevsMin.append(reviewFrame[reviewFrame['minDist'] == i]['rating'].std())
    numsMin.append(reviewFrame[reviewFrame['minDist'] == i]['rating'].shape[0])
    stdErrorsMin.append(stdDevsMin[-1]/math.sqrt(numsMin[-1]))

fig = plt.figure()
fig.set_facecolor("white")
p = plt.errorbar(
    range(1, 8),
    meansMin,
    marker="o",
    color="blue",
    yerr=stdErrorsMin)
plt.xlim([0, 8])
plt.ylabel('Avg Rating of Paper')
plt.xlabel('Min Distance between Reviewer and Paper Authors')
fig.suptitle('Avg Rating Given Min Distance')

meansAvg = []
stdDevsAvg = []
numsAvg = []
stdErrorsAvg = []
for i in range(1, 8):
    meansAvg.append(reviewFrame[(reviewFrame['avgDist'] >= i - 0.5) & (reviewFrame['avgDist'] < i + 0.5)]['rating'].mean())
    stdDevsAvg.append(reviewFrame[(reviewFrame['avgDist'] >= i - 0.5) & (reviewFrame['avgDist'] < i + 0.5)]['rating'].std())
    numsAvg.append(reviewFrame[(reviewFrame['avgDist'] >= i - 0.5) & (reviewFrame['avgDist'] < i + 0.5)]['rating'].shape[0])
    stdErrorsAvg.append(stdDevsAvg[-1]/math.sqrt(numsAvg[-1]))

fig = plt.figure()
fig.set_facecolor("white")
p = plt.errorbar(
    range(1, 8),
    meansAvg,
    marker="o",
    color="red",
    yerr=stdErrorsAvg)
plt.xlim([0, 8])
plt.ylabel('Avg Rating of Paper')
plt.xlabel('Avg Distance between Reviewer and Paper Authors')
fig.suptitle('Avg Rating Given Avg Distance')

plotBucket(
    reviewFrame,
    "avgDist",
    "rating",
    delta=10,
    y_label="Avg Rating of Paper",
    x_label="Avg Distance between Reviewer and Paper Authors",
    color="red",
    x_percentile=False)


# plt.figure(22)
# plt.scatter(reviewsWithHistory['numPastPapers'], reviewsWithHistory['rating'] + np.random.normal(loc=0, scale=0.2, size=2971),
#     c = ['red' if a else 'blue' for a in reviewsWithHistory['accepted']])

meansPaper = []
stdDevsPaper = []
numsPaper = []
stdErrorsPaper = []
bins = [0, 5, 10, 20, 40, 80, 160, 320, 640]
for i in range(len(bins) - 1):
    meansPaper.append(reviewsWithHistory[(reviewsWithHistory['avgPastPapers'] >= bins[i]) &
        (reviewsWithHistory['avgPastPapers'] >= bins[i+1])]['rating'].mean())
    stdDevsPaper.append(reviewsWithHistory[(reviewsWithHistory['numPastPapers'] >= bins[i]) &
        (reviewsWithHistory['avgPastPapers'] >= bins[i+1])]['rating'].std())
    numsPaper.append(reviewsWithHistory[(reviewsWithHistory['avgPastPapers'] >= bins[i]) &
        (reviewsWithHistory['avgPastPapers'] >= bins[i+1])]['rating'].shape[0])
    stdErrorsPaper.append(stdDevsPaper[-1]/math.sqrt(numsPaper[-1]))
fig = plt.figure()
fig.set_facecolor('white')
p = plt.errorbar(
    range(len(bins) - 1),
    meansPaper,
    marker="o",
    color="red",
    yerr=stdErrorsPaper)
xticks(range(len(bins) - 1), bins[:-1])


# plt.figure(21)
# h, x, y = np.histogram2d(reviewsWithHistory['rating'], reviewsWithHistory['numPastPapers'],
#     bins=([-3.5, -2.5, -1.5, 0, 1.5, 2.5, 3.5], [0, 5, 10, 20, 40, 80, 160, 320, 640]))
# rowsums = h.sum(axis=1)
# h = h/rowsums[:, np.newaxis]
# plt.pcolor(h, cmap='Greys')
# plt.yticks(range(len(x)), x)
# plt.xticks(range(len(y)), y)
# plt.ylabel('rating')
# plt.xlabel('number of past publications')

# fig = plt.figure(1)
# heatmap1, x, y = np.histogram2d(reviewFrame['confidence'], reviewFrame['rating'],
#     bins=([0.5, 1.5, 2.5, 3.5],[-3.5, -2.5, -1.5, 0, 1.5, 2.5, 3.5]))
# rowsums = heatmap1.sum(axis=1)
# confRatingHeatmap = heatmap1/rowsums[:, np.newaxis]
# plt.pcolor(confRatingHeatmap, cmap='Greys')
# plt.yticks(range(len(x)), x)
# plt.xticks(range(len(y)), y)
# plt.xlabel('rating')
# plt.ylabel('confidence')
# fig.suptitle('Rating Given Confidence in Paper Subject Area')

# plt.figure(2)
# heatmap2, xedges, yedges = np.histogram2d(reviewFrame['novelty'], reviewFrame['rating'], bins=(5,7))
# rowsums = heatmap2.sum(axis=1)
# novRatingHeatmap = np.nan_to_num(heatmap2/rowsums[:, np.newaxis])
# plt.pcolor(novRatingHeatmap, cmap='Greys')
# plt.xlabel('rating')
# plt.ylabel('novelty')

# plt.figure(3)
# heatmap3, xedges, yedges = np.histogram2d(reviewFrame['technicalDevelopment'], reviewFrame['rating'], bins=(5,7))
# rowsums = heatmap3.sum(axis=1)
# tdRatingHeatmap = np.nan_to_num(heatmap3/rowsums[:, np.newaxis])
# plt.pcolor(tdRatingHeatmap, cmap='Greys')
# plt.xlabel('rating')
# plt.ylabel('tech development')

# plt.figure(4)
# heatmap4, xedges, yedges = np.histogram2d(reviewFrame['presentation'], reviewFrame['rating'], bins=(5,7))
# rowsums = heatmap4.sum(axis=1)
# presRatingHeatmap = np.nan_to_num(heatmap4/rowsums[:, np.newaxis])
# plt.pcolor(presRatingHeatmap, cmap='Greys')
# plt.xlabel('rating')
# plt.ylabel('presentation')

# plt.figure(5)
# heatmap5, xedges, yedges = np.histogram2d(reviewFrame['rating'], reviewFrame['novelty'], bins=(7,5))
# rowsums = heatmap5.sum(axis=1)
# ratingNovHeatmap = np.nan_to_num(heatmap5/rowsums[:, np.newaxis])
# plt.pcolor(ratingNovHeatmap, cmap='Greys')
# plt.xlabel('novelty')
# plt.ylabel('rating')

# plt.figure(6)
# heatmap6, xedges, yedges = np.histogram2d(reviewFrame['rating'], reviewFrame['technicalDevelopment'], bins=(7,5))
# rowsums = heatmap6.sum(axis=1)
# ratingTdHeatmap = np.nan_to_num(heatmap6/rowsums[:, np.newaxis])
# plt.pcolor(ratingTdHeatmap, cmap='Greys')
# plt.xlabel('tech development')
# plt.ylabel('rating')

# plt.figure(7)
# heatmap7, xedges, yedges = np.histogram2d(reviewFrame['rating'], reviewFrame['presentation'], bins=(7,5))
# rowsums = heatmap7.sum(axis=1)
# ratingPresHeatmap = np.nan_to_num(heatmap7/rowsums[:, np.newaxis])
# plt.pcolor(ratingPresHeatmap, cmap='Greys')
# plt.xlabel('presentation')
# plt.ylabel('rating')

# fig = plt.figure(8)
# h, x, y = np.histogram2d(reviewsWithBids['value'], reviewsWithBids['confidence'],
#     bins=([-0.5, 0.5, 1.5, 2.5, 3.5],[0.5, 1.5, 2.5, 3.5]))
# rowsums = h.sum(axis=1)
# bidConfHeatmap = h/rowsums[:, np.newaxis]
# plt.pcolor(bidConfHeatmap, cmap='Greys')
# plt.yticks(range(len(x)), x)
# plt.xticks(range(len(y)), y)
# plt.xlabel('confidence')
# plt.ylabel('bid')
# fig.suptitle('Confidence in Paper Subject Area Given Bid')

# fig = plt.figure(12)
# h, x, y = np.histogram2d(reviewsWithBids['confidence'], reviewsWithBids['value'],
#     bins=([0.5, 1.5, 2.5, 3.5], [-0.5, 0.5, 1.5, 2.5, 3.5]))
# rowsums = h.sum(axis=1)
# confBidHeatmap = h/rowsums[:, np.newaxis]
# plt.pcolor(confBidHeatmap, cmap='Greys')
# plt.yticks(range(len(x)), x)
# plt.xticks(range(len(y)), y)
# plt.xlabel('bid')
# plt.ylabel('confidence')
# fig.suptitle('Bid Given Confidence in Paper Subject Area')

# fig = plt.figure(13)
# h, x, y = np.histogram2d(reviewsWithBids['value'], reviewsWithBids['rating'],
#     bins=([-0.5, 0.5, 1.5, 2.5, 3.5],[-3.5, -2.5, -1.5, 0, 1.5, 2.5, 3.5]))
# rowsums = h.sum(axis=1)
# bidRatingHeatmap = h/rowsums[:, np.newaxis]
# plt.pcolor(bidRatingHeatmap, cmap='Greys')
# plt.yticks(range(len(x)), x)
# plt.xticks(range(len(y)), y)
# plt.xlabel('rating')
# plt.ylabel('bid')
# fig.suptitle('Rating Given Bid')

# fig = plt.figure(14)
# h, x, y = np.histogram2d(reviewsWithBids['rating'], reviewsWithBids['value'],
#     bins=([-3.5, -2.5, -1.5, 0, 1.5, 2.5, 3.5], [-0.5, 0.5, 1.5, 2.5, 3.5]))
# rowsums = h.sum(axis=1)
# ratingBidHeatmap = h/rowsums[:, np.newaxis]
# plt.pcolor(ratingBidHeatmap, cmap='Greys')
# plt.yticks(range(len(x)), x)
# plt.xticks(range(len(y)), y)
# plt.xlabel('bid')
# plt.ylabel('rating')
# fig.suptitle('Bid Given Rating')

# plt.figure(9)
# plt.scatter(paperFrame['avgRating'], paperFrame['metaRating'])
# plt.figure(10)
# plt.scatter(paperFrame['avgBid'], paperFrame['avgRating'])
# plt.figure(11)
# plt.scatter(paperFrame['numBids'], paperFrame['avgRating'])

show()
