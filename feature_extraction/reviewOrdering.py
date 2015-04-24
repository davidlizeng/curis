import warnings
import numpy as np
import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
    import numpy as np

from feature_extraction import calcFeatures
from feature_extraction.dataLoader import DataLoader
from utilities.plotBucket import plotBucket
from utilities.plotBucket import plotBar
from utilities.plotBucket import plotFrequencyHistogram

loader = DataLoader()
loader.loadUsers()
loader.loadPapers()
loader.loadPastPapers()
loader.loadAcceptance()
loader.loadReviews()

paperTable = []
paperToOrder = defaultdict(list)
reviewerOrder = {}
reviewerOrder1 = {}
reviewerOrder2 = {}

def countInversions(a):
  count = 0
  for i in xrange(len(a)):
    for j in xrange(i+1, len(a)):
      if a[i] > a[j]:
        count += 1
  return count

inversions = {}
less_scramble = set()
more_scramble = set()
for id, reviewer in loader.reviewers.iteritems():
  revs = reviewer.reviews
  if len(revs) > 7:
    sorted_rev = sorted(revs, key=lambda x: int(x.time.strftime('%s')))
    paperIds = [r.paper.id for r in sorted_rev]
    numInv = countInversions(paperIds)
    inversions[id] = numInv
    if numInv > 15:
      more_scramble.add(id)
    else:
      less_scramble.add(id)
df_order = pd.DataFrame(inversions.values())
df_order.columns = ['order_stat']
plotFrequencyHistogram(df_order, 'order_stat', "# perm inversions", myBins=np.linspace(0, 50, 10))


df_paper = pd.read_pickle(
    "savedFrames/iteration5/paperTable")
df_review = pd.read_pickle(
    "savedFrames/iteration5/reviewTable")
df = pd.merge(df_review, df_paper, on="paperId")
df['time'] = df['time'].values.astype(datetime.datetime)
df["agree"] = (df["rating"] > 0) == df["accepted"]
df["positive"] = df["rating"] > 0
df["absRating"] = df["rating"].abs()
df_less = df[df['userId'].isin(less_scramble)]
df_more = df[df['userId'].isin(more_scramble)]


def transformDates(dateLabels):
    return list(pd.Series([
        datetime.datetime.strptime(d + '/2014', '%m/%d/%Y')
        for d in dateLabels
    ]).values.astype(datetime.datetime))


def plotDeadline(yoffset=10):
    deadline = '4/15'
    plt.plot(
        transformDates([deadline]) * 2,
        plt.ylim(),
        color="gray",
        linestyle="--",
        linewidth=2,
        alpha=.8)
    plt.text(
        transformDates([deadline])[0],
        plt.ylim()[1] - yoffset,
        "  Review Submission\n  Deadline",
        va="top",
        color="gray",
        alpha=.8)


labels_month = ['3/20', '3/30', '4/10', '4/20', '4/30']
dates_month = transformDates(labels_month)


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
    plotMean=False,
)
plotBucket(
    df_more,
    'time',
    'rating',
    numBuckets=5,
    x_percentile=False,
    title='Rating v. Submission Date',
    x_label="Submission Date",
    y_label="Average Review Rating",
    color="red",
    sameFigure=True,
    plotMean=False,
)
plotBucket(
    df_less,
    'time',
    'rating',
    numBuckets=5,
    x_percentile=False,
    title='Rating v. Submission Date',
    x_label="Submission Date",
    y_label="Average Review Rating",
    color="green",
    sameFigure=True,
    plotMean=False,
)
plt.xticks(dates_month, labels_month)
#plt.xticks(dates_5Days, labels_5Days)
#plt.xlim([dates_5Days[0], dates_5Days[-1]])
plotDeadline(.1)

#Plot 4 -- Submission Time vs. P(Positive)
plotBucket(
    df,
    'time',
    'positive',
    numBuckets=5,
    x_percentile=False,
    title='Positive Ratings v. Submission Date',
    x_label="Submission Date",
    y_label="Proportion of Ratings that were Positive",
    plotMean=False,
)
plotBucket(
    df_more,
    'time',
    'positive',
    numBuckets=5,
    x_percentile=False,
    title='Positive Ratings v. Submission Date',
    x_label="Submission Date",
    y_label="Proportion of Ratings that were Positive",
    sameFigure=True,
    color="red",
    plotMean=False,
)
plotBucket(
    df_less,
    'time',
    'positive',
    numBuckets=5,
    x_percentile=False,
    title='Positive Ratings v. Submission Date',
    x_label="Submission Date",
    y_label="Proportion of Ratings that were Positive",
    sameFigure=True,
    color="green",
    plotMean=False,
)
plt.xticks(dates_month, labels_month)
plotDeadline(.1)

#Plot 5 -- Submission Time vs. Magnitude
plotBucket(
    df,
    'time',
    'absRating',
    numBuckets=7,
    x_percentile=False,
    title='Rating Magnitude v. Submission Date',
    x_label="Submission Date",
    y_label="Rating Magnitude",
    plotMean=False,
)
plotBucket(
    df_more,
    'time',
    'absRating',
    numBuckets=7,
    x_percentile=False,
    title='Rating Magnitude v. Submission Date',
    x_label="Submission Date",
    y_label="Rating Magnitude",
    sameFigure=True,
    color="red",
    plotMean=False,
)
plotBucket(
    df_less,
    'time',
    'absRating',
    numBuckets=7,
    x_percentile=False,
    title='Rating Magnitude v. Submission Date',
    x_label="Submission Date",
    y_label="Rating Magnitude",
    sameFigure=True,
    color="green",
    plotMean=False,
)
plt.xticks(dates_month, labels_month)
plotDeadline(.1)

# #Plot 6 -- Submission Time vs. Each Rating
# ratingDict = {
#     -3: "Strong Reject",
#     -2: "Reject",
#     -1: "Weak Reject",
#     1: "Weak Accept",
#     2: "Accept",
#     3: "Strong Accept",
# }

# legendLabels = [
#     "Reject & Strong Reject",
#     "Weak Reject",
#     "Weak Accept",
#     "Accept & Strong Accept"
# ]

# colors = ["red", "", "orange", "",  "blue", "green"]
# p = []
# for r in [[-2, -3], [-1], [1], [2, 3]]:
#     df["currRating"] = df["rating"].isin(r)
#     p.append(plotBucket(
#         df,
#         'time',
#         'currRating',
#         numBuckets=6 if len(r) == 1 else 5,
#         color=colors[min(r)+3],
#         x_percentile=False,
#         title='Rating Type v. Submission Date',
#         x_label="Submission Date",
#         y_label="Proportion of Ratings",
#         sameFigure=(min(r) != -3),
#         plotMean=False
#     ))
# plt.xticks(dates_month, labels_month)
# plt.xlim(transformDates(["4/7", "4/23"]))
# plotDeadline(.05)
# plt.ylim([-0.1, 0.5])
# plt.legend(p, legendLabels, loc=4)

#Plot 7 -- Submission Time vs. Influence
p = []
legendLabels = [
    "All Reviewers",
    "Random Order Reviewers",
    "In Order Reviewers",
]
p.append(plotBucket(
    df,
    'time',
    'agree',
    numBuckets=10,
    x_percentile=False,
    title='Review Influence v. Submission Date',
    x_label="Submission Date",
    y_label="Proportion of Reviews that Agree with Outcome",
    plotMean=False,
))
p.append(plotBucket(
    df_more,
    'time',
    'agree',
    numBuckets=8,
    x_percentile=False,
    title='Review Influence v. Submission Date',
    x_label="Submission Date",
    y_label="Proportion of Reviews that Agree with Outcome",
    color="red",
    sameFigure=True,
    plotMean=False,
))
p.append(plotBucket(
    df_less,
    'time',
    'agree',
    numBuckets=8,
    x_percentile=False,
    title='Review Influence v. Submission Date',
    x_label="Submission Date",
    y_label="Proportion of Reviews that Agree with Outcome",
    color="green",
    sameFigure=True,
    plotMean=False,
))
plt.ylim([.7, .9])

labels = ["4/%d" % d for d in np.arange(13, 20)]
plt.xticks(transformDates(labels), labels)
plt.xlim(transformDates(["4/12", "4/19"]))
plotDeadline(.05)
plt.legend(p, legendLabels, loc=1)


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
    plotMean=False,
)
plotBucket(
    df_more,
    'time',
    'reviewLength',
    numBuckets=10,
    x_percentile=False,
    sameFigure=True,
    color="red",
    title='Review Length v. Submission Date',
    x_label="Submission Date",
    y_label="Review Length (words)",
    plotMean=False,
)
plotBucket(
    df_less,
    'time',
    'reviewLength',
    numBuckets=10,
    x_percentile=False,
    sameFigure=True,
    color="green",
    title='Review Length v. Submission Date',
    x_label="Submission Date",
    y_label="Review Length (words)",
    plotMean=False,
)

#labels = ["4/6", "4/10", "4/14", "4/16", "4/18"]
#plt.xticks(transformDates(labels), labels)
#plt.xlim(transformDates(["4/5", "4/20"]))

plt.xticks(dates_5Days[1:], labels_5Days[1:])
plt.xlim([dates_5Days[0], dates_5Days[-1]])
plotDeadline()


# cutoff = int(datetime.datetime(2014, 4, 15, 0, 0).strftime('%s'))
# lateReviewers = []
# goodReviewers = []
# for id, reviewer in loader.reviewers.iteritems():
#   revs = reviewer.reviews
#   lateCount = 0
#   for r in revs:
#     submit = int(r.time.strftime('%s'))
#     if submit > cutoff:
#       lateCount += 1
#   if len(revs) > 0 and lateCount < 2:
#     goodReviewers.append(reviewer)
#   elif len(revs) > 0:
#     lateReviewers.append(reviewer)

# print len(goodReviewers), len(lateReviewers)

# goodReviewerOrder = {}
# lateReviewerOrder = {}
# for reviewer in goodReviewers:
#   revs = reviewer.reviews
#   if len(revs) > 8:
#     sorted_rev = sorted(revs, key=lambda x: int(x.time.strftime('%s')))
#     # goodReviewerOrder[reviewer.id] = quicksort([r.paper.id for r in sorted_rev], 0, len(revs) - 1)[0]
#     pos = np.argsort([r.paper.id for r in sorted_rev])
#     n = 1.0 * len(pos)
#     goodReviewerOrder[reviewer.id] = ((np.arange(n) - pos)**2).sum()
#     goodReviewerOrder[reviewer.id] /= (2 * n + n ** 3) / 3
# for reviewer in lateReviewers:
#   revs = reviewer.reviews
#   if len(revs) > 8:
#     sorted_rev = sorted(revs, key=lambda x: int(x.time.strftime('%s')))
#     # lateReviewerOrder[reviewer.id] = quicksort([r.paper.id for r in sorted_rev], 0, len(revs) - 1)[0]
#     pos = np.argsort([r.paper.id for r in sorted_rev])
#     n = 1.0 * len(pos)
#     lateReviewerOrder[reviewer.id] = ((np.arange(n) - pos)**2).sum()
#     lateReviewerOrder[reviewer.id] /= (2 * n + n ** 3) / 3

# for id, reviewer in loader.reviewers.iteritems():
#   revs = reviewer.reviews
#   if len(revs) > 0:
#     sorted_rev = sorted(revs, key=lambda x: int(x.time.strftime('%s')))
#     pos = np.argsort([r.paper.id for r in sorted_rev])
#     n = 1.0 * len(pos)
#     reviewerOrder[id] = ((np.arange(n) - pos)**2).sum()
#     reviewerOrder[id] /= (2 * n + n ** 3) / 3

#     if len(revs) > 8:
      # reviewerOrder[id] = quicksort([r.paper.id for r in sorted_rev], 0, len(revs) - 1)[0]

      # len1 = 4 #min(5, len(revs))
      # pos1 = np.argsort([r.paper.id for r in sorted_rev[0:len1]])
      # reviewerOrder1[id] = ((np.arange(len1) - pos1)**2).sum() * 1.0
      # reviewerOrder1[id] /= (2 * len1 + len1 ** 3) / 3.0
      # reviewerOrder1[id] = quicksort([r.paper.id for r in sorted_rev[0:4]], 0, 3)[0]


      # len2 = 4 #len(revs) - 5
      # pos2 = np.argsort([r.paper.id for r in sorted_rev[4:8]])
      # reviewerOrder2[id] = ((np.arange(len2) - pos2)**2).sum() * 1.0
      # reviewerOrder2[id] /= (2 * len2 + len2 ** 3) / 3.0
      # reviewerOrder2[id] = quicksort([r.paper.id for r in sorted_rev[4:8]], 0, 3)[0]

# df_order = DataFrame(reviewerOrder.values())
# df_order.columns = ['order_stat']
# # plotFrequencyHistogram(df_order, 'order_stat', "Order Statistic", myBins=np.linspace(0, 20, 10))
# plotFrequencyHistogram(df_order, 'order_stat', "Order Statistic", myBins=np.linspace(0, 1, 6))

# df_order_late = DataFrame(lateReviewerOrder.values())
# df_order_late.columns = ['order_stat']
# # plotFrequencyHistogram(df_order_late, 'order_stat', "Order Statistic Late", myBins=np.linspace(0, 20, 10))
# plotFrequencyHistogram(df_order_late, 'order_stat', "Order Statistic Late", myBins=np.linspace(0, 1, 6))

# df_order_good = DataFrame(goodReviewerOrder.values())
# df_order_good.columns = ['order_stat']
# # plotFrequencyHistogram(df_order_good, 'order_stat', "Order Statistic On Time", myBins=np.linspace(0, 20, 10))
# plotFrequencyHistogram(df_order_good, 'order_stat', "Order Statistic On Time", myBins=np.linspace(0, 1, 6))

# df_order1 = DataFrame(reviewerOrder1.values())
# df_order1.columns = ['order_stat']
# plotFrequencyHistogram(df_order1, 'order_stat', "Quicksort swaps first 4", myBins=np.linspace(0, 4, 4))

# df_order2 = DataFrame(reviewerOrder2.values())
# df_order2.columns = ['order_stat']
# plotFrequencyHistogram(df_order2, 'order_stat', "Quicksort swaps next 4", myBins=np.linspace(0, 4, 4))

# for id, paper in loader.papers.iteritems():
#   revs = paper.reviews
#   if len(revs) > 0:
#     submissionTimes = np.array([
#         int(r.time.strftime('%s'))
#         for r in revs])
#     averageTime = np.datetime64(
#         datetime.datetime.fromtimestamp(
#             submissionTimes.mean()
#         )
#     )
#     orderStats = {
#       "paperId": id,
#       "avgReviewTime": averageTime,
#       "avgReviewOrder": np.array(paperToOrder[id]).mean()
#     }
#     paperTable.append(orderStats)

# df = DataFrame(paperTable)
# plt.figure()
# plt.plot(
#   df['paperId'],
#   df['avgReviewOrder'],
#   'o'
# )

# def quicksort(lista,izq,der):
#   i = izq
#   j = der
#   swap_count = 0
#   compare_count = 0
#   pivote = lista[(izq + der)//2]

#   while i <= j:
#     while lista[i] < pivote:
#       i += 1
#     while pivote < lista[j]:
#       j -= 1
#     if i < j:
#       aux = lista[i]
#       lista[i] = lista[j]
#       lista[j] = aux
#       swap_count += 1
#       i += 1
#       j -= 1
#     elif i == j:
#       i += 1
#       j -= 1
#     compare_count += 1

#   if izq < j:
#     other_swap, other_compare = quicksort(lista, izq, j)
#     swap_count += other_swap
#     compare_count += other_compare
#   if i < der:
#     other_swap, other_compare = quicksort(lista, i, der)
#     swap_count += other_swap
#     compare_count += other_compare

#   return (swap_count, compare_count)
plt.show()
