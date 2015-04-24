import warnings
from feature_extraction import calcFeatures
import numpy as np

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from pandas import DataFrame

from feature_extraction.dataLoader import DataLoader
from feature_extraction.tfIdf import tf_idf

loader = DataLoader()
loader.loadAll()
loader.loadClassifierAccuracy()

#loader.loadAll()

tfidf = tf_idf()
tfidf.store_tf_idf(loader)

print "Calculating Features"
calcFeatures.calcUsersAccepted(loader)
calcFeatures.calcAuthorsPastPapers(loader)
calcFeatures.computeAverages(loader)
calcFeatures.computeDistances(loader.reviews)
#calcFeatures.calcWeightedPaperCount(loader)
calcFeatures.calcTopConfsJoursCount(loader)

print "Constructing Author Table"
authorTable = []

for id, user in loader.users.iteritems():
    if len(user.papers) == 0:
        continue
    authorTable.append({
        "userId": id,
        "affiliation": user.affiliation,
        "acceptanceRate": user.numAccepted*1.0/len(user.papers),
        "topPastPapers": user.topPastPapers,
        "connectivity": user.connectivity
    })

print "Constructing Paper Table"
paperTable = []

for id, paper in loader.papers.iteritems():

    pastPaperCounts = [len(a.pastPapers) for a in paper.authors]
    pastPaperCounts.sort(reverse=True)
    maxTopAuthor = sorted(paper.authors, key=lambda a: a.topPastPapers)[-1]

    paperTable.append({
        "paperId": paper.id,

        "avgRating": paper.avgRating,
        "accepted": paper.accepted,

        "authorCountryMode": calcFeatures.getAuthorCountryMode(paper),

        ###past paper counts of authors
        "paperCountAvg": np.mean(pastPaperCounts),
        "paperCountMax": pastPaperCounts[0],
        "paperCountPrimary": len(paper.primaryAuthor.pastPapers),

        ###top paper counts of authors
        "topPaperCountAvg": sum(a.topPastPapers for a in paper.authors) * 1.0 / len(paper.authors),
        "topPaperCountMax": maxTopAuthor.topPastPapers,
        "topPaperCountPrimary": paper.primaryAuthor.topPastPapers,

        "paperCount2ndHighest":
        pastPaperCounts[1] if len(pastPaperCounts) > 1 else -1,

        ###authors
        "numAuthors": len(paper.authors),
        "authorCountryMode": calcFeatures.getAuthorCountryMode(paper),

        ###subject area
        "subjectAreaPrimaryGeneral": paper.primaryGeneralSubjectArea,

        ###classifier accuracy
        "accuracyReviewText": paper.classifierAccReviews,
        "accuracyAbstract": paper.classifierAccAbstract,
        "abstractClassifierProb": paper.classifierProbAbstract,
        "abstractLength": len(paper.abstract.split()),

        ###Connectivity
        "connectivity": paper.maxConnectivity,
        "degreeCentrality": paper.maxDegCenter,
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

        "paperCountReviewer": len(reviewer.pastPapers),

        ###Similarity

        "similarityPrimary": calcFeatures.getAuthorReviewerSimilarity(
            tfidf, paper.primaryAuthor, reviewer),

        "similarityMax": calcFeatures.getAuthorReviewerSimilarity(
            tfidf, paper.maxAuthor, reviewer),

        # "similarityMaxJaccard": calcFeatures.getAuthorReviewerSimilarity(
        #     tfidf, paper.maxAuthor, reviewer, jaccard=True),

        # "similarityPrimaryJaccard": calcFeatures.getAuthorReviewerSimilarity(
        #     tfidf, paper.primaryAuthor, reviewer, jaccard=True),

        ###Co-Author Distance
        "distMin": review.minDist,
        "distSecondMin": review.secondMinDist,
        "distAvg": review.avgDist,
        "distMaxAuthor": review.distMaxAuthor,
        "distPrimary": review.distPrimary,

        ###Deviations
        "devPaperMean": review.overallRating - paper.avgRating,

        ###Review Stats
        "reviewLength": len(
            ("%s %s %s" % (
                review.ratings["strengths"],
                review.ratings["weaknesses"],
                review.ratings["comments"])).split()),
        "externalReviewer": review.externalReviewer,

        "countryReviewer": reviewer.country,
        "countryAuthorMode": calcFeatures.getAuthorCountryMode(paper),
        "countryAuthorPrimary": paper.primaryAuthor.country,

        "time": np.datetime64(review.time),

        ###classifier accuracy
        "accuracyAcceptance": review.classifierAccAccept,
        "accuracyRating": review.classifierAccRating
    })

    i += 1
    if i % 250 == 0:
        print "(%d/%d) Reviews Completed" % (i, len(loader.reviews))

DataFrame(paperTable).to_pickle("savedFrames/iteration5/paperTable")
DataFrame(reviewTable).to_pickle("savedFrames/iteration5/reviewTable")
DataFrame(authorTable).to_pickle("savedFrames/iteration5/authorTable")
