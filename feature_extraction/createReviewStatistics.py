import warnings
import numpy as np

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from pandas import DataFrame

from feature_extraction.dataLoader import DataLoader

loader = DataLoader()
loader.loadAll()

reviewTable = []
metaReviewTable = []
bidTable = []
paperTable = []
userTable = []

for id, review in loader.reviews.iteritems():
    maxDist = 7
    sumDist = 0
    dists = []
    for author in review.paper.authors:
        if author.id in review.user.distances:
            dist = review.user.distances[author.id]
            sumDist += dist

            dists.append(dist)
        else:
            sumDist += maxDist
    dists.sort()
    while len(dists) < 4:
        dists.append(maxDist)

    reviewStats = {
        "userId": review.user.id,
        "paperId": review.paper.id,
        "confidence": review.confidence,
        "rating": review.overallRating,
        "novelty": review.ratings['novelty'],
        "technicalDevelopment": review.ratings['technicalDevelopment'],
        "presentation": review.ratings['presentation'],
        "avgDist": 1.0*sumDist/len(review.paper.authors),
        "minDist": dists[0],
        "secondMinDist": dists[1],
        "thirdMinDist": dists[2],
        "fourthMinDist": dists[3]
    }
    reviewTable.append(reviewStats)

for id, metaReview in loader.metaReviews.iteritems():
    metaReviewStats = {
        "userId": metaReview.user.id,
        "paperId": metaReview.paper.id,
        "rating": metaReview.overallRating,
    }
    metaReviewTable.append(metaReviewStats)

for id, paper in loader.papers.iteritems():
    paperStats = {
        "paperId": id,
        "avgBid": np.nan if len(paper.bids) == 0 else 1.0*sum(paper.bids.values())/len(paper.bids),
        "avgRating": np.nan if len(paper.reviews) == 0 else 1.0*sum(r.overallRating for r in paper.reviews)/len(paper.reviews),
        "metaRating": np.nan if len(paper.metaReviews) == 0 else 1.0*sum(m.overallRating for m in paper.metaReviews)/len(paper.metaReviews),
        "maxPastPapers": max(a.pastPapers for a in paper.authors),
        "avgPastPapers": 1.0*sum(len(a.pastPapers) for a in paper.authors)/len(paper.authors),
        "numBids": len(paper.bids),
        "accepted": paper.accepted,
    }
    paperTable.append(paperStats)
    for userId, bid in paper.bids.iteritems():
        bidStats = {
            "userId": userId,
            "paperId": id,
            "value": bid,
        }
        bidTable.append(bidStats)

for id, user in loader.users.iteritems():
    userStats = {
        "userId": id,
        "numPastPapers": len(user.pastPapers),
    }
    userTable.append(userStats)

DataFrame(reviewTable).to_pickle(
    "savedFrames/reviewStatistics/reviewTable")
DataFrame(metaReviewTable).to_pickle(
    "savedFrames/reviewStatistics/metaReviewTable")
DataFrame(bidTable).to_pickle(
    "savedFrames/reviewStatistics/bidTable")
DataFrame(paperTable).to_pickle(
    "savedFrames/reviewStatistics/paperTable")
DataFrame(userTable).to_pickle(
    "savedFrames/reviewStatistics/userTable")
