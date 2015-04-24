from feature_extraction.dataLoader import DataLoader
from feature_extraction.tfIdf import tf_idf
from scipy.sparse import *
from scipy import io
from scipy import *
import cPickle
from collections import defaultdict

print "Begin Loading Data"
loader = DataLoader()
loader.loadUsers()
loader.loadPapers()
loader.loadPastPapers()
loader.loadAbstracts()
print "End Loading Data"


print "Begin Computing TF-IDF Vectors"
tfidf = tf_idf()
tfidf.store_tf_idf(loader, allPapers=True)
print "End Computing TF-IDF Vectors"


#Rows in Matrix
m = len(loader.papers) + len(loader.pastPapers)
#Initial Columns in Matrix
n = [100000]
currRow = [0]


#Term -> term id dictionary
def incrementAndReturn():
    currId[0] += 1
    return currId[0]
currId = [-1]
termDict = defaultdict(incrementAndReturn)

X = dok_matrix((m, n[0]), dtype=float32)


def processPaperdict(paperdict):
    for id, paper in paperdict.iteritems():
        if not paper.tfVector is None:
            for term, value in paper.tfVector.iteritems():
                termId = termDict[term]
                X[currRow[0], termId] = value
            currRow[0] += 1

            if currRow[0] % 1000 == 0:
                print "%d Vectors Added of %d" % (currRow[0], m)
                if currId[0] + 10000 > n[0]:
                    n[0] += 50000
                    X.resize((m, n[0]))

print "%d Vectors Added of %d" % (currRow[0], m)
processPaperdict(loader.papers)
processPaperdict(loader.pastPapers)
print "%d Vectors Added of %d" % (currRow[0], m)
X.resize((m, currId[0]+1))

print "Saving first file"
f = open("savedFrames/clusteringMatrix.mat", 'wb')
cPickle.dump(X, f)
f.close()
print "Saving second file"
f = open("savedFrames/clusteringTermDict.dat", 'wb')
cPickle.dump(dict(termDict), f)
f.close()