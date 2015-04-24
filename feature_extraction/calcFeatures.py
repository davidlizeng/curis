###FILE USED TO COMPUTE STATISTICS WITH LOADED DATA
from sets import Set
import math
from collections import defaultdict
#import snap
import codecs


#takes a DataLoader object
#gives each a user a field "accepted"
#which is a boolean indicating whether one of their papers was accepted
#gives each user a field "numAccepted"
#which is an int indicating the number of papers that have been accepted
def calcUsersAccepted(loader):

    for id, user in loader.users.iteritems():
        hasPaperAccepted = False
        numAccepted = 0
        for paper in user.papers:
            if paper.accepted:
                hasPaperAccepted = True
                numAccepted += 1

        user.accepted = hasPaperAccepted
        user.numAccepted = numAccepted


#gives each paper a field "avgRating"
#a float of the average of all overall rating scores given to the paper
#gives each paper a field "varRating"
#a float of the variance of all overall rating scores given to the paper
#None if there are less than 3 ratings
def calcRatingMoments(loader):
    for id, paper in loader.papers.iteritems():

        sumRatings = 0
        sumSquaredRatings = 0
        num = 0

        for review in paper.reviews:
            if not review.overallRating is None:
                sumRatings += review.overallRating
                sumSquaredRatings += review.overallRating**2
                num += 1

        if num == 0:
            avgRating = None
            varRating = None
        else:
            avgRating = sumRatings * 1.0 / num

            if num < 3:
                varRating = None
            else:
                sumSquaredRatings = sumSquaredRatings * 1.0 / num
                varRating = sumSquaredRatings - avgRating ** 2

        paper.varRating = varRating
        paper.avgRating = avgRating


#gives each paper a field "varRating"
#a float of the variance of all overall rating scores given to the paper
#None if there are less than 3 ratings
def calcVarRating(loader):
    for id, paper in loader.papers.iteritems():
        sumRatings = 0
        sumSquaredRatings = 0
        num = 0

        for review in paper.reviews:
            if not review.overallRating is None:
                sumRatings += review.overallRating
                sumSquaredRatings += review.overallRating**2
                num += 1

        if num < 3:
            paper.varRating = None
        else:

            sumRatings = sumRatings * 1.0 / num
            sumSquaredRatings = sumSquaredRatings * 1.0 / num

            paper.varRating = sumSquaredRatings - sumRatings ** 2


#gives each paper a field "authorsPastPaperCount"
#an int indicating the sum of the papers' authors past paper counts
#gives each paper a field "authorsMaxPastPaper"
#an int indicating the max past papers of the authors
#gives each paper a field "maxAuthor"
#a user that has the max past papers of the authors
def calcAuthorsPastPapers(loader):
    for id, paper in loader.papers.iteritems():
        sumPastPapers = 0
        maxPastPapers = 0
        maxAuthor = None

        for author in paper.authors:
            count = len(author.pastPapers)
            sumPastPapers += len(author.pastPapers)

            if count >= maxPastPapers:
                maxPastPapers = count
                maxAuthor = author

        paper.authorsPastPaperCount = sumPastPapers
        paper.authorsMaxPastPaper = maxPastPapers
        paper.maxAuthor = maxAuthor


#uses tfidf to compute average cosine similarity between
#the paper and the reviewer's past papers
def computePaperReviewerSimilarity(tfidf, paper, reviewer):
    return tfidf.computeSimilarity(paper, reviewer)


def getAuthorReviewerSimilarity(tfidf, author, reviewer, jaccard=False):
    return tfidf.computeSimilarity(author, reviewer, jaccard)


def computeSpecificCommonSubjects(paper, reviewer):
    return len(
        Set(paper.specificSubjectAreas).intersection(
            Set(reviewer.specificSubjectAreas)))


def computeGeneralCommonSubjects(paper, reviewer):
    return len(
        paper.generalSubjectAreas.intersection(
            reviewer.generalSubjectAreas))


#gives each paper a field avgRating
#a float indicating the average overallrating from it's reviews and meta reviews
#gives each reviewer a field avgRating
#a float indicating the average overall rating the reviewer gives in his reviews
def computeAverages(loader):
    for id, paper in loader.papers.iteritems():
        storeAvg(paper)

    for id, reviewer in loader.reviewers.iteritems():
        storeAvg(reviewer)


#helper method for above
def storeAvg(obj):
    sum = 0.0
    n = 0.0

    for r in obj.reviews:
        n += 1
        sum += r.overallRating
    for r in obj.metaReviews:
        n += 1
        sum += r.overallRating
    if n > 0:
        obj.avgRating = sum * 1.0 / n
    else:
        obj.avgRating = 0


#compute jaccard similarity
def computeJaccard(list1, list2):
    set1 = Set(list1)
    set2 = Set(list2)

    return len(set1.intersection(set2)) * 1.0 / len(set1.union(set2))


#returns mode country of paper authors
def getAuthorCountryMode(paper):
    countryFreqs = defaultdict(lambda: 0)

    for author in paper.authors:
        countryFreqs[author.country] += 1

    mode = 0
    modeCountry = None

    for country, count in countryFreqs.iteritems():
        if count > mode:
            modeCountry = country
            mode = count

    return modeCountry

#returns whether all authors of paper were from industry, academia, or both
def getAcademicOrIndustry(paper):
    isAcademic = [author.isAcademic for author in paper.authors]
    if all(isAcademic):
        return 'Academic'
    if not any(isAcademic):
        return 'Industry'
    else:
        return 'Mixed'



#returns best similarity from all users
def getBestSimilarity(tfidf, author, users):
    maxScore = 0

    for id, user in users.iteritems():
        if id != author.id:
            score = tfidf.computeSimilarity(author, user)

            if (score > maxScore):
                maxScore = score

    return maxScore


#gives each reviewer a field weakInfluence
#number of times that a rating agreed with outcome
#gives each reviewer a field strongInfluence
#number of times that a rating of value >= 2 agreed with outcome
#gives each reviewer a field numStrongReviews
#number of times that a reviewer gives a value of >= 2
def calcReviewerInfluence(loader):
    for id, user in loader.reviewers.iteritems():
        numWeak = 0
        numStrong = 0
        numAgreedWeak = 0
        numAgreedStrong = 0
        numPos = 0
        numPosAgreed = 0
        numDevAgreed = 0

        for review in user.reviews:
            isStrong = math.fabs(review.overallRating) >= 2
            agrees = (review.overallRating > 0) == review.paper.accepted
            isPos = review.overallRating > 0

            if isStrong:
                numStrong += 1
            if agrees:
                if isStrong:
                    numAgreedStrong += 1
                if isPos:
                    numPosAgreed += 1
                numAgreedWeak += 1

            if ((review.overallRating > user.firstMoment) == review.paper.accepted):
                numDevAgreed += 1

            if isPos:
                numPos += 1
            numWeak += 1

        user.weakInfluence = numAgreedWeak
        user.strongInfluence = numAgreedStrong
        user.numStrongReviews = numStrong
        user.posReviews = numPos
        user.posInfluence = numPosAgreed
        user.deviationInfluence = numDevAgreed


#gives each reviewer a field avgDeviation
#average deviation from paper mean
def calcReviewerAvgDeviation(loader):
    for id, user in loader.reviewers.iteritems():
        totalDeviation = 0.0
        totalReviews = 0.0
        totalRating = 0.0
        totalRatingSq = 0.0

        for review in user.reviews:
            totalDeviation += review.overallRating - review.paper.avgRating
            totalRatingSq += review.overallRating ** 2
            totalRating += review.overallRating
            totalReviews += 1

        if totalReviews > 0:
            user.avgDeviation = totalDeviation / totalReviews
            user.firstMoment = totalRating / totalReviews
            user.secondMoment = totalRatingSq / totalReviews
        else:
            user.avgDeviation = 0
            user.firstMoment = 0
            user.secondMoment = 0


#gives each user a field weightedPaperCount
def calcWeightedPaperCount(loader):
    freq = defaultdict(lambda: 0)

    for id, paper in loader.pastPapers.iteritems():
        freq[paper.name] += 1

    freq["CoRR"] = 0

    for id, user in loader.users.iteritems():
        total = 0

        for paper in user.pastPapers:
            total += freq[paper.name]

        user.weightedPaperCount = total

    for id, paper in loader.papers.iteritems():

        paper.maxWeightedPaperCount = \
            max(paper.authors, key=lambda a: a.weightedPaperCount)\
            .weightedPaperCount


def calcTopConfsJoursCount(loader):
    topSet = Set()
    file = open("csv/topConfsJours.csv")
    for line in file:
        topSet.add(line[:-1])

    for id, user in loader.users.iteritems():
        total = 0
        kdd = 0
        nips = 0
        sigir = 0
        sigmod = 0
        icml = 0
        icde = 0
        icdm = 0

        for paper in user.pastPapers:
            total += paper.name in topSet
            kdd += paper.name == "KDD"
            nips += paper.name == "NIPS"
            sigir += paper.name == "SIGIR"
            sigmod += paper.name == "SIGMOD Conference"
            icml += paper.name == "ICML"
            icde += paper.name == "ICDE"
            icdm += paper.name == "ICDM"

        user.topPastPapers = total
        user.topKDDPast = kdd
        user.topNIPSPast = nips
        user.topSIGIRPast = sigir
        user.topSIGMODPast = sigmod
        user.topICMLPast = icml
        user.topICDEPast = icde
        user.topICDMPast = icdm


#Calculates distance metrics for reviews
def computeDistances(reviews):
    for id, review in reviews.iteritems():
        paper = review.paper
        reviewer = review.user


        maxDist = 7
        sumDist = 0
        dists = []
        for author in paper.authors:
            if author.id in reviewer.distances:
                dist = reviewer.distances[author.id]
                sumDist += dist

                dists.append(dist)
            else:
                sumDist += maxDist
        dists.sort()

        review.avgDist = 1.0*sumDist/len(review.paper.authors)
        while len(dists) < 4:
            dists.append(maxDist)

        review.minDist = dists[0]
        review.secondMinDist = dists[1]

        if reviewer.id in paper.maxAuthor.distances:
            review.distMaxAuthor = paper.maxAuthor.distances[reviewer.id]
        else:
            review.distMaxAuthor = 7
        if reviewer.id in paper.primaryAuthor.distances:
            review.distPrimary = paper.primaryAuthor.distances[reviewer.id]
        else:
            review.distPrimary = 7


def getPaperDistStats(paper):

    if len(paper.reviews) > 0:

        minDists = [review.minDist for review in paper.reviews]
        avgDists = [review.avgDist for review in paper.reviews]

        stats = {
            "minDist": min(minDists),
            "avgMinDist": sum(minDists)*1.0/len(minDists),
            "avgDist": sum(avgDists)*1.0/len(avgDists),
            "minAvgDist": min(avgDists)
        }
        return stats

    else:
        return defaultdict(lambda: 0)


def getSimStats(paper, tfidf):
    if len(paper.reviews) > 0:

        simScores = [
            [
                getAuthorReviewerSimilarity(tfidf, author, review.user)
                for author in paper.authors
            ]
            for review in paper.reviews
        ]

        maxSimilarities = [max(a) for a in simScores]
        avgSimilarities = [sum(a)*1.0/len(a) for a in simScores]

        stats = {
            "avgSim": sum(avgSimilarities)*1.0/len(avgSimilarities),
            "maxSim": max(maxSimilarities),
            "avgMaxSim": sum(maxSimilarities)*1.0/len(maxSimilarities)
        }
        return stats

    else:
        return defaultdict(lambda: 0)

def calcAuthorStructure(loader):
    outfile = open("authorStructures", "w")
    fin = snap.TFIn('coauthor.graph')
    graph = snap.TNEANet.Load(fin)
    nameToNId = {}
    uIdToNId = {}
    for n in graph.Nodes():
        id = n.GetId()
        nameToNId[graph.GetStrAttrDatN(id, 'name').decode('utf-8')] = id
    infile = codecs.open('csv/dblpusersaff.csv', 'r', 'utf-8')
    lines = infile.read().splitlines()
    infile.close()
    for line in lines:
        tokens = line.split('||')
        if tokens[2] != '':
            uIdToNId[int(tokens[0])] = nameToNId[tokens[1]]
    for id, p in loader.papers.iteritems():
        sumDist = 0
        connections = 0
        density = 0
        avgDist = 0
        dblp = []
        for a in p.authors:
            if a.id in uIdToNId:
                dblp.append(a)
        components = defaultdict(int)
        for a in dblp:
            compSize = 0
            dists = snap.TIntH()
            snap.GetShortPath(graph, uIdToNId[a.id], dists)

            for b in dblp:
                if uIdToNId[b.id] in dists:
                    sumDist += dists[uIdToNId[b.id]]
                    compSize += 1
                    connections += 1
            components[compSize] += 1
        for size in components:
            components[size] /= size

        if len(dblp) > 1:
            density = connections*1.0/(len(dblp) * (len(dblp) - 1))
        if connections > 0:
            avgDist = sumDist*1.0/connections
        orphans = len(p.authors) - len(dblp)
        outfile.write("%d %d %d %d %f %f\n" %(id, orphans, len(components), connections, density, avgDist))
        for size, num in components.iteritems():
            outfile.write("%d %d\n" %(size, num))
        outfile.flush()
        print id
    outfile.close()
