import warnings
from feature_extraction import calcFeatures

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from pandas import DataFrame

from feature_extraction.dataLoader import DataLoader

loader = DataLoader()
loader.loadAll()

calcFeatures.calcUsersAccepted(loader)
calcFeatures.calcRatingMoments(loader)
calcFeatures.calcAuthorsPastPapers(loader)

calcFeatures.calcReviewerAvgDeviation(loader)
calcFeatures.calcReviewerInfluence(loader)

#Some User Statistics
userTable = []

for id, user in loader.users.iteritems():
    userStats = {
        "userId": user.id,
        "inDBLP?": len(user.dblpKey) > 0,
        "#Papers": len(user.papers),
        "#PastPapers": len(user.pastPapers),
        "#PastPapersPrimaryAuthor": len(user.papersPrimary),
        "hasAcceptedPaper": user.accepted,
        "#Accepted": user.numAccepted,
        "#Siblings": user.numSiblings,
        "#Cousins": user.numCousins,
    }
    userTable.append(userStats)

reviewerTable = []

for id, reviewer in loader.reviewers.iteritems():
    reviewerStats = {
        "userId": reviewer.id,
        "#Bids": len(reviewer.bids),
        "primarySpecificSubjectArea": reviewer.primarySpecificSubjectArea,
        "primarySubjectArea": reviewer.primaryGeneralSubjectArea,
        "numReviews": len(reviewer.reviews),
        "numStrongReviews": reviewer.numStrongReviews,
        "weakInfluence": reviewer.weakInfluence,
        "strongInfluence": reviewer.strongInfluence,
        "posInfluence": reviewer.posInfluence,
        "deviationInfluence": reviewer.deviationInfluence,
        "posReviews": reviewer.posReviews,
        "numPastPapers": len(reviewer.pastPapers),
        "avgDeviation": reviewer.avgDeviation,
        "rating2ndMoment": reviewer.secondMoment,
        "ratingMean": reviewer.firstMoment
    }
    reviewerTable.append(reviewerStats)

papersTable = []

for id, paper in loader.papers.iteritems():
    paperStats = {
        "paperId": paper.id,
        "primarySpecificSubjectArea": paper.primarySpecificSubjectArea,
        "primarySubjectArea": paper.primaryGeneralSubjectArea,
        "abstractWordCount": len(paper.abstract.split()),
        "titleWordCount": len(paper.title.split()),
        "studentPaper?": paper.isStudent,
        "accepted": paper.accepted,
        "#Bids": len(paper.bids),
        "#Authors": len(paper.authors),
        "avgRating": paper.avgRating,
        "varRating": paper.varRating,
        "authorsPastPaperCount": paper.authorsPastPaperCount,
        "authorsMaxPastPaper": paper.authorsMaxPastPaper,
        "primaryAuthorPastPaperCount": len(paper.primaryAuthor.pastPapers),
        "maxAuthorCountry": paper.maxAuthor.country,
        "authorCountryMode": calcFeatures.getAuthorCountryMode(paper),
        "primaryAuthorCountry": paper.primaryAuthor.country,
        "academicOrIndustry": calcFeatures.getAcademicOrIndustry(paper),
        "maxAuthorAcademicOrIndustry": paper.maxAuthor.isAcademic,
        "maxConnectivity": paper.maxConnectivity,
        "maxPageRank": paper.maxPageRank,
        "maxDegCenter": paper.maxDegCenter,
    }
    papersTable.append(paperStats)

DataFrame(userTable).to_pickle(
    "savedFrames/summaryStatistics/userTable")
DataFrame(reviewerTable).to_pickle(
    "savedFrames/summaryStatistics/reviewerTable")
DataFrame(papersTable).to_pickle(
    "savedFrames/summaryStatistics/papersTable")
