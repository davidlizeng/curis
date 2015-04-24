import cPickle
from sklearn.cluster import MiniBatchKMeans
from sklearn import metrics
from time import time

print "Loading first file"
f = open("savedFrames/clusteringMatrix.mat", 'r')
X = cPickle.load(f)
print X.shape
f.close()
print "Loading second file"
f = open("savedFrames/clusteringTermDict.dat", 'r')
termDict = cPickle.load(f)
f.close()

reverseDict = {}
for k, v in termDict.iteritems():
    reverseDict[v] = k


ks = range(15)[14:]

for k in ks:
    km = MiniBatchKMeans(n_clusters=k)
    print("Clustering sparse data with %d clusters" % k)
    t0 = time()
    km.fit(X)
    print("done in %0.3fs" % (time() - t0))
    print("Top terms per cluster:")
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    for i in range(k):
        print("Cluster %d:" % i)
        for ind in order_centroids[i, :10]:
            print(' %s' % reverseDict[ind])
        print()