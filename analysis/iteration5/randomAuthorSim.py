import warnings
from pylab import *
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
    import numpy as np
from feature_extraction.dataLoader import DataLoader
from feature_extraction import calcFeatures
from utilities.plotBucket import plotBucket
from utilities.plotBucket import plotBar
from utilities.plotBucket import plotFrequencyHistogram
import math
import random

loader = DataLoader()
loader.loadAll(distance = False)
print "Calculating Features"
calcFeatures.calcAuthorsPastPapers(loader)
calcFeatures.calcTopConfsJoursCount(loader)
calcFeatures.computeAverages(loader)

df = pd.read_pickle(
    "savedFrames/predictionFeatures/paperTable")
exp = 'maxTopPaperCount'
target = 'avgRating'

numBuckets = 7
percentiles = (100.0/numBuckets)*np.arange(numBuckets + 1)
buckets = np.percentile(df[exp].values, percentiles.tolist())
buckets[0] = -1
averages = []
for i in range(numBuckets):
    avg = df[(df[exp] > buckets[i]) & (df[exp] <= buckets[i + 1])][target].mean()
    averages.append(avg)

def getAvg(exp):
    for i in range(len(buckets) - 1):
        if exp > buckets[i] and exp <= buckets[i + 1]:
            return averages[i]

authorExpList = []
numAuthorsList = []
for id, paper in loader.papers.iteritems():
    numAuthorsList.append(len(paper.authors))
    for a in paper.authors:
        authorExpList.append(a.topPastPapers)

numRuns = 500
avgRatings = []
errors = []
for i in range(1, max(numAuthorsList) + 1):
    ratings = np.empty([numRuns, 1])
    for j in range(numRuns):
        sample = random.sample(authorExpList, i)
        maxExp = max(sample)
        ratings[j] = getAvg(maxExp)
    avgRatings.append(ratings.mean())
    errors.append(ratings.std()/math.sqrt(ratings.shape[0]))

p1 = plotBar(
    df,
    "numAuthors",
    "avgRating",
    range(1, 8),
    color="green",
    x_label="Number of Authors",
    y_label="Average Rating",
    marker="o",
    plotMean=False,
)
p2 = plt.errorbar(np.arange(1, 8), avgRatings[:7], yerr=errors[:7], marker = 'o')
plt.xlim([0,8])
plt.legend((p1, p2), ('Real', 'Simulated'), loc=4)
plt.show()
