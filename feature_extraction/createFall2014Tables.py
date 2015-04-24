import warnings
from feature_extraction import calcFeatures
import numpy as np
from collections import defaultdict

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from pandas import DataFrame

from feature_extraction.dataLoader import DataLoader

loader = DataLoader()
loader.loadAll()

print "Constructing Reviewer Table"
reviewerTable = []

for id, user in loader.reviewers.iteritems():

    if len(user.papers) == 0:
        continue

    reviewerTable.append({
        "userId": id,
        "numPastPapers": len(user.pastPapers),
        "dateFirstPaper": min([p.year for p in user.pastPapers]),
        "numBids": len(user.bids),
    })


print "Constructing Paper Table"
paperTable = []

for id, paper in loader.papers.iteritems():

    paperTable.append({
        "paperId": paper.id,

        "accepted": paper.accepted,
    })

print "Constructing Review Table"
i = 0
reviewTable = []

for id, review in loader.reviews.iteritems():
    paper = review.paper
    reviewer = review.user

    reviewTable.append({
        "paperId": paper.id,
        "userId": reviewer.id,

        "rating": review.overallRating,

        ###Review Stats
        "reviewLength": len(
            ("%s %s %s" % (
                review.ratings["strengths"],
                review.ratings["weaknesses"],
                review.ratings["comments"])).split()),

        "time": np.datetime64(review.time),

    })

#very inefficient code for quickly computing the order with which a review was given
times = defaultdict(list)
for review in reviewTable:
    times[review["userId"]].append(review["time"])
for k in times:
    times[k].sort()
for review in reviewTable:
    review["order"] = times[review["userId"]].index(review["time"])+1

DataFrame(reviewerTable).to_pickle("savedFrames/fall2014/reviewerTable")
DataFrame(paperTable).to_pickle("savedFrames/fall2014/paperTable")
DataFrame(reviewTable).to_pickle("savedFrames/fall2014/reviewTable")
