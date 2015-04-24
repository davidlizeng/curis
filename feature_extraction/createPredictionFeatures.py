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
tfidf = tf_idf()
tfidf.store_tf_idf(loader)

print "Calculating Features"
calcFeatures.calcAuthorsPastPapers(loader)
calcFeatures.calcTopConfsJoursCount(loader)
calcFeatures.computeAverages(loader)
calcFeatures.computeDistances(loader.reviews)


print "Constructing Paper Table"
paperTable = []

for id, paper in loader.papers.iteritems():

    maxAuthor = sorted(paper.authors, key=lambda a: len(a.pastPapers))[-1]
    maxTopAuthor = sorted(paper.authors, key=lambda a: a.topPastPapers)[-1]
    maxKDDAuthor = sorted(paper.authors, key=lambda a: a.topKDDPast)[-1]
    numAuthors = len(paper.authors)
    affiliation = calcFeatures.getAcademicOrIndustry(paper)

    distStats = calcFeatures.getPaperDistStats(paper)
    simStats = calcFeatures.getSimStats(paper, tfidf)

    paperTable.append({
        "paperId": paper.id,

        ###true values
        "avgRating": paper.avgRating,
        "accepted": paper.accepted,

        ###nationalities of authors
        "modeAuthorCountry": calcFeatures.getAuthorCountryMode(paper),
        "maxAuthorCountry": maxAuthor.country,
        "primaryAuthorCountry": paper.primaryAuthor.country,

        ###affiliation of team of authors

        "isIndustry": int(affiliation == 'industry'),
        "isAcademic": int(affiliation == 'academic'),
        "isMixed": int(affiliation == 'mixed'),

        ###past paper counts of authors
        "avgPaperCount": sum(len(a.pastPapers) for a in paper.authors) * 1.0 / numAuthors,
        "maxPaperCount": len(maxAuthor.pastPapers),
        "primaryPaperCount": len(paper.primaryAuthor.pastPapers),
        "avgLogPaperCount":  np.log([len(a.pastPapers) for a in paper.authors]).sum() / numAuthors,

        ###top paper counts of authors
        "avgTopPaperCount": sum(a.topPastPapers for a in paper.authors) * 1.0 / numAuthors,
        "maxTopPaperCount": maxTopAuthor.topPastPapers,
        "primaryTopPaperCount": paper.primaryAuthor.topPastPapers,
        "avgLogTopPaperCount":  np.log([a.topPastPapers for a in paper.authors]).sum() / numAuthors,

        ###KDD paper counts of authors
        "avgKDDPaperCount": sum(a.topKDDPast for a in paper.authors) * 1.0 / numAuthors,
        "maxKDDPaperCount": maxTopAuthor.topKDDPast,
        "primaryKDDPaperCount": paper.primaryAuthor.topKDDPast,

        ###NIPS paper counts of authors
        "avgNIPSPaperCount": sum(a.topNIPSPast for a in paper.authors) * 1.0 / numAuthors,
        "maxNIPSPaperCount": maxTopAuthor.topNIPSPast,
        "primaryNIPSPaperCount": paper.primaryAuthor.topNIPSPast,

        ###SIGIR paper counts of authors
        "avgSIGIRPaperCount": sum(a.topSIGIRPast for a in paper.authors) * 1.0 / numAuthors,
        "maxSIGIRPaperCount": maxTopAuthor.topSIGIRPast,
        "primarySIGIRPaperCount": paper.primaryAuthor.topSIGIRPast,

        ###SIGMOD paper counts of authors
        "avgSIGMODPaperCount": sum(a.topSIGMODPast for a in paper.authors) * 1.0 / numAuthors,
        "maxSIGMODPaperCount": maxTopAuthor.topSIGMODPast,
        "primarySIGMODPaperCount": paper.primaryAuthor.topSIGMODPast,

        ###ICML paper counts of authors
        "avgICMLPaperCount": sum(a.topICMLPast for a in paper.authors) * 1.0 / numAuthors,
        "maxICMLPaperCount": maxTopAuthor.topICMLPast,
        "primaryICMLPaperCount": paper.primaryAuthor.topICMLPast,

        ###ICDE paper counts of authors
        "avgICDEPaperCount": sum(a.topICDEPast for a in paper.authors) * 1.0 / numAuthors,
        "maxICDEPaperCount": maxTopAuthor.topICDEPast,
        "primaryICDEPaperCount": paper.primaryAuthor.topICDEPast,

        ###ICDM paper counts of authors
        "avgICDMPaperCount": sum(a.topICDMPast for a in paper.authors) * 1.0 / numAuthors,
        "maxICDMPaperCount": maxTopAuthor.topICDMPast,
        "primaryICDMPaperCount": paper.primaryAuthor.topICDMPast,

        ###Centrality measures of authors
        "maxConnectivity": paper.maxConnectivity,
        "maxPageRank": paper.maxPageRank,
        "maxDegCentrality": paper.maxDegCenter,

        ###Number of authors
        "numAuthors": numAuthors,
        "numNoDBLP": paper.noDBLP,
        "numCC": paper.numCC,
        "numConn": paper.numConn,
        "density": paper.density,
        "avgDist": paper.avgDist,
        "avgCCSize": paper.avgSize,
        "maxCCSize": paper.maxSize,

        ###Reviewer Summary Statistics
        "hasReviews": len(paper.reviews) > 0,

        "minDist": distStats["minDist"],
        "avgMinDist": distStats["avgMinDist"],
        "minAvgDist": distStats["minAvgDist"],
        "avgDist": distStats["avgDist"],

        "avgSimilarity": simStats["avgSim"],
        "maxSimilarity": simStats["maxSim"],
        "avgMaxSimilarity": simStats["avgMaxSim"],
    })

df = DataFrame(paperTable)
logColumns = ["avgLogPaperCount", "avgLogTopPaperCount"]
for i in logColumns:
    df.loc[df[i] < -1, i] = -1

toLog = [
    "avgPaperCount",
    "maxPaperCount",
    "primaryPaperCount",
    "avgTopPaperCount",
    "maxTopPaperCount",
    "primaryTopPaperCount",
    "avgKDDPaperCount",
    "maxKDDPaperCount",
    "primaryKDDPaperCount",
    "avgNIPSPaperCount",
    "maxNIPSPaperCount",
    "primaryNIPSPaperCount",
    "avgSIGIRPaperCount",
    "maxSIGIRPaperCount",
    "primarySIGIRPaperCount",
    "avgSIGMODPaperCount",
    "maxSIGMODPaperCount",
    "primarySIGMODPaperCount",
    "avgICMLPaperCount",
    "maxICMLPaperCount",
    "primaryICMLPaperCount",
    "avgICDEPaperCount",
    "maxICDEPaperCount",
    "primaryICDEPaperCount",
    "avgICDMPaperCount",
    "maxICDMPaperCount",
    "primaryICDMPaperCount",
    "maxConnectivity",
    "maxPageRank",
    "maxDegCentrality",
    "numAuthors"
]

for i in toLog:
    il = i+"Log"
    df[il] = df[i]
    df.loc[df[il] == 0, il] = .1
    df.loc[:, il] = np.log(df.loc[:, il])

df.to_pickle("savedFrames/predictionFeatures/paperTable")


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

        "revPaperCount": len(reviewer.pastPapers),
        "revTopPaperCount": reviewer.topPastPapers,
        "revKDDPaperCount": reviewer.topKDDPast,

        ###Similarity
        "maxSimilarity": calcFeatures.getAuthorReviewerSimilarity(
            tfidf, paper.maxAuthor, reviewer),

        "primarySimilarity": calcFeatures.getAuthorReviewerSimilarity(
            tfidf, paper.primaryAuthor, reviewer),

        "maxJacSimilarity": calcFeatures.getAuthorReviewerSimilarity(
            tfidf, paper.maxAuthor, reviewer, jaccard=True),

        "primaryJacSimilarity": calcFeatures.getAuthorReviewerSimilarity(
            tfidf, paper.primaryAuthor, reviewer, jaccard=True),

        ###Co-Author Distance
        "minDist": review.minDist,
        "avgDist": review.avgDist,

        "revCountry": reviewer.country,
    })

    i += 1
    if i % 250 == 0:
        print "(%d/%d) Reviews Completed" % (i, len(loader.reviews))

df = DataFrame(reviewTable)

toLog = [
    "revPaperCount",
    "revTopPaperCount",
    "revKDDPaperCount",
]

for i in toLog:
    il = i+"Log"
    df[il] = df[i]
    df.loc[df[il] == 0, il] = .1
    df.loc[:, il] = np.log(df.loc[:, il])

df.to_pickle("savedFrames/predictionFeatures/reviewTable")
