from feature_extraction.dataLoader import DataLoader
from feature_extraction.tfIdf import tf_idf
from scipy.sparse import dok_matrix
from scipy import *
import cPickle
from collections import defaultdict
from sets import Set

steps = 7

#LOAD IN DATA
print "(1/%d) Loading Data" % steps
loader = DataLoader()
loader.loadUsers()
loader.loadPastPapers()
loader.loadPapers()
loader.loadAcceptance()

#COMPUTE IDF
print "(2/%d) Computing IDF" % steps
tfidf = tf_idf()
tfidf.computeIdf(loader)


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


##Produce Matrix for Abstracts
threshold = 30
termCounts = defaultdict(lambda: 0)
allowedTerms = Set()

print "(3/%d) Computing Per Paper Vectors" % steps
paperIds = []
paperVectors = []
for id, paper in loader.papers.iteritems():
    v, l = tfidf.getVector([paper.title, paper.abstract])

    for term in l:
        termCounts[term] += 1

    paperIds.append(id)
    paperVectors.append(v)

for term, count in termCounts.iteritems():
    if count >= threshold:
        allowedTerms.add(term)

print "(4/%d) Computing Per Paper Matrix" % steps
paperMatrix = getSparseMatrix(paperVectors, termDict, currId)


##SAVE ALL FIIVE FILES
def saveFile(obj, name):
    f = open("savedFrames/iteration5/abstractPrediction/"+name, 'wb')
    cPickle.dump(obj, f)
    f.close()

print "(5/%d) Saving Term Dict" % steps
saveFile(dict(termDict), "termDict.dat")

print "(6/%d) Saving Paper Ids" % steps
saveFile(paperIds, "paperIds.dat")

print "(7/%d) Saving Paper Matrix" % steps
saveFile(paperMatrix, "paperMatrix.mat")
