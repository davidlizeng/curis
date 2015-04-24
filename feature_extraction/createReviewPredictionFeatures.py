from feature_extraction.dataLoader import DataLoader
from feature_extraction.tfIdf import tf_idf
from scipy.sparse import dok_matrix
from scipy import *
import cPickle
from collections import defaultdict
from sets import Set

steps = 11

#LOAD IN DATA
print "(1/%d) Loading Data" % steps
loader = DataLoader()
loader.loadUsers()
loader.loadPapers()
loader.loadPastPapers()
loader.loadReviews()
loader.loadAcceptance()

#COMPUTE IDF
print "(2/%d) Computing IDF" % steps
tfidf = tf_idf()
tfidf.computeIdf(loader, [
    r.getReviewText()
    for id, r in loader.reviews.iteritems()
])


#SET UP TERM DICTIONARY
def incrementAndReturn():
    currId[0] += 1
    return currId[0]
currId = [-1]
termDict = defaultdict(incrementAndReturn)


#FUNCTION TO BUILD MATRICES
def getSparseMatrix(vectors, termDict, currId):
    n = len(vectors)
    m = currId[0]+1 if currId[0] > 0 else 100000

    X = dok_matrix((n, m), dtype=float32)

    for i, v in enumerate(vectors):
        for term, value in v.iteritems():
            termId = termDict[term]
            if term in allowedTerms:
                X[i, termId] = value

        if i % 300 == 0:
            print "    %d Vectors Added of %d" % (i, n)

    X.resize((n, currId[0]+1))

    print "    Features Used: %d" % (len(allowedTerms))

    return X


##FIRST TRY COMBINING ALL REVIEWS
threshold = 100
termCounts = defaultdict(lambda: 0)
allowedTerms = Set()

print "(3/%d) Computing Per Paper Vectors" % steps
paperIds = []
paperTexts = []
fields = ["comments", "strengths", "weaknesses"]
paperVectors = [[], [], []]

for id, paper in loader.papers.iteritems():
    if len(paper.reviews) > 0:
        textList = [
            review.getReviewText()
            for review in paper.reviews
        ]

        v, l = tfidf.getVector(textList)
        paperIds.append(id)
        paperTexts.append(v)

        for term in l:
            termCounts[term] += 1

        for i in range(3):
            v, l = tfidf.getVector([review.ratings[fields[i]] for review in paper.reviews])
            paperVectors[i].append(v)


for term, count in termCounts.iteritems():
    if count >= threshold:
        #print term
        allowedTerms.add(term)

print "(4/%d) Computing Per Paper Matrix" % steps
paperTextMatrix = getSparseMatrix(paperTexts, termDict, currId)
paperMatrices = [getSparseMatrix(v, termDict, currId) for v in paperVectors]
paperMatrixNames = ["paperCommentMatrix.mat", "paperStrengthMatrix.mat", "paperWeaknessMatrix.mat"]

##Now Each Review Individually
print "(5/%d) Computing Per Review Vectors" % steps
reviewInfo = []
reviewTexts = []
reviewVectors = [[], [], []]

for id, r in loader.reviews.iteritems():
    v, l = tfidf.getVector([r.getReviewText()])

    reviewInfo.append(r.id)
    reviewTexts.append(v)

    for i in range(3):
        v, l = tfidf.getVector([r.ratings[fields[i]]])
        reviewVectors[i].append(v)

print "(6/%d) Computing Per Review Matrix" % steps
reviewTextMatrix = getSparseMatrix(reviewTexts, termDict, currId)
reviewMatrices = [getSparseMatrix(v, termDict, currId) for v in reviewVectors]
reviewMatrixNames = ["reviewCommentMatrix.mat", "reviewStrengthMatrix.mat", "reviewWeaknessMatrix.mat"]

##SAVE ALL FIIVE FILES
def saveFile(obj, name):
    f = open("savedFrames/iteration5/reviewPrediction/"+name, 'wb')
    cPickle.dump(obj, f)
    f.close()

print "(7/%d) Saving Term Dict" % steps
saveFile(dict(termDict), "termDict.dat")

print "(8/%d) Saving Paper Ids" % steps
saveFile(paperIds, "paperIds.dat")

print "(9/%d) Saving Paper Matrix" % steps
saveFile(paperTextMatrix, "paperTextMatrix.mat")
[saveFile(paperMatrices[i], paperMatrixNames[i]) for i in range(3)]

print "(10/%d) Saving Review Info" % steps
saveFile(reviewInfo, "reviewInfo.dat")

print "(11/%d) Saving Review Matrix" % steps
saveFile(reviewTextMatrix, "reviewTextMatrix.mat")
[saveFile(reviewMatrices[i], reviewMatrixNames[i]) for i in range(3)]
