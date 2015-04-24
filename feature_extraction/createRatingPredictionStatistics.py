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

calcFeatures.calcAuthorsPastPapers(loader)
calcFeatures.computeAverages(loader)
calcFeatures.calcWeightedPaperCount(loader)
calcFeatures.calcTopConfsJoursCount(loader)

#Some User Statistics
ratingTable = []

print "Building Review Table"
print "There are %d reviews" % len(loader.reviews)

for id, review in loader.reviews.iteritems():
    paper = review.paper
    reviewer = review.user
    ratingStats = {
        "rating": review.overallRating,
        "time": np.datetime64(review.time),
        "pastPaperSimilarity": calcFeatures.computePaperReviewerSimilarity(
            tfidf, paper, reviewer),

        "authorReviewerSimilarity": calcFeatures.getAuthorReviewerSimilarity(
            tfidf, paper.primaryAuthor, reviewer),

        "maxAuthorReviewerSimilarity": calcFeatures.getAuthorReviewerSimilarity(
            tfidf, paper.maxAuthor, reviewer),

        "specificCommonSubjects": calcFeatures.computeSpecificCommonSubjects(
            paper, reviewer),

        "generalCommonSubjects": calcFeatures.computeGeneralCommonSubjects(
            paper, reviewer),

        "samePrimaryGeneralSubject":
        reviewer.primaryGeneralSubjectArea == paper.primaryGeneralSubjectArea,

        "samePrimarySpecificSubject":
        reviewer.primarySpecificSubjectArea == paper.primarySpecificSubjectArea,

        "jaccardSpecificSubjects": calcFeatures.computeJaccard(
            paper.specificSubjectAreas, reviewer.specificSubjectAreas),
        "jaccardGeneralSubjects": calcFeatures.computeJaccard(
            paper.generalSubjectAreas, reviewer.generalSubjectAreas),

        "reviewerPastPaperCount": len(reviewer.pastPapers),

        "abstractWordCount": len(paper.abstract.split()),
        "titleWordCount": len(paper.title.split()),
        "#Authors": len(paper.authors),
        "authorsPastPaperCount": paper.authorsPastPaperCount,
        "authorsMaxPastPaper": paper.authorsMaxPastPaper,
        "maxWeightedCount": paper.maxWeightedPaperCount,
        "avgTopCount": paper.avgTopCount,
        "priTopCount": paper.priTopCount,
        "maxTopCount": paper.maxTopCount,
        "maxKDDCount": paper.maxKDDCount,
        "primaryAuthorPastPaperCount": len(paper.primaryAuthor.pastPapers),
        "accepted": paper.accepted,

        "reviewerAverage": reviewer.avgRating,
        "paperAverage": paper.avgRating,
        "reviewerRatingDiff": review.overallRating - reviewer.avgRating,
        "paperRatingDiff": review.overallRating - paper.avgRating,
        "paperId": paper.id,
        "userId": reviewer.id,

        "reviewLength": len(
            ("%s %s %s" % (
                review.ratings["strengths"],
                review.ratings["weaknesses"],
                review.ratings["comments"])).split()),
        "externalReviewer": review.externalReviewer,

        "reviewerCountry": reviewer.country,
        "authorCountryMode": calcFeatures.getAuthorCountryMode(paper),
        "primaryAuthorCountry": paper.primaryAuthor.country,

        "reviewerIsAcademic": reviewer.isAcademic,
        "paperAcademicOrIndustry": calcFeatures.getAcademicOrIndustry(paper),
        "maxAuthorIsAcademic": paper.maxAuthor.isAcademic,
    }
    ratingTable.append(ratingStats)

    if id % 100 == 0 and id > 0:
        print id

DataFrame(ratingTable).to_pickle("savedFrames/ratingPrediction/ratingTable")
