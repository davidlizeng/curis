import warnings
from feature_extraction import calcFeatures

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

paperTable = []

print "Building Paper Table"
print "There are %d papers" % len(loader.papers)

for id, paper in loader.papers.iteritems():
    mostSimilarStats = {
        "paperId": paper.id,

        "bestSimilarityOfReviewers":
        calcFeatures.getBestSimilarity(
            tfidf, paper.maxAuthor, loader.reviewers),

        "bestSimilarityOfAuthors":
        calcFeatures.getBestSimilarity(
            tfidf, paper.maxAuthor, loader.users)
    }

    paperTable.append(mostSimilarStats)

    if id % 10 == 0 and id > 0:
        print id

DataFrame(paperTable).to_pickle(
    "savedFrames/ratingPrediction/mostSimilarTable")
