from models.user import *
from models.paper import *
from models.pastPaper import *
from models.review import *
import os
import datetime

usersFile = "csv/dblpusersaff.csv"
papersFile = "csv/papers.csv"
usersPapersJoinFile = "csv/papersusers.csv"
pastPapersConferencesFile = "csv/dblpconfs.csv"
pastPapersJournalsFile = "csv/dblpjours.csv"
pastPapersUsersJoinFile = "csv/dblpuserspapers.csv"
bidsFile = "csv/bids.tsv"
subjectAreasFiles = "csv/subjectareas.tsv"
reviewsFile = "csv/reviews/ReviewsRevised.tsv"
metaReviewsFile = "csv/reviews/MetaReviewerRevised.tsv"
acceptanceFile = "csv/acceptedPapers.csv"
abstractsFolder = "../abstracts"
distanceFile = "csv/distances6.csv"
connectivityFile = "csv/connectivity.csv"
centralitiesFile = "csv/centralities.csv"
timeFile = "csv/reviews/review_dates.txt"
structureFile = "authorStructures"
likesFile = "csv/likes.csv"


class DataLoader(object):

    def __init__(self):
        self.loadedUsers = False
        self.loadedPapers = False
        self.loadedPastPapers = False
        self.loadedSubjectAreas = False
        self.loadedReviews = False

        self.users = {}
        self.reviewers = {}
        self.papers = {}
        self.pastPapers = {}
        self.reviews = {}
        self.metaReviews = {}

    def loadAll(self, distance=True):
        print "(0/10) Begin Loading"
        print "(1/10) Loading Users"
        self.loadUsers()
        assert self.loadedUsers
        print "(2/10) Loading Papers"
        self.loadPapers()
        assert self.loadedPapers
        print "(3/10) Loading Past Papers"
        self.loadPastPapers()
        assert self.loadedPastPapers
        print "(4/10) Loading Subject Areas"
        self.loadSubjectAreas()
        assert self.loadedSubjectAreas
        print "(5/10) Loading Reviews"
        self.loadReviews()
        assert self.loadedReviews
        print "(6/10) Loading Acceptances"
        self.loadAcceptance()
        print "(7/10) Loading Distances"
        if distance:
            self.loadDistance()
        print "(8/10) Loading Abstracts"
        self.loadAbstracts()
        print "(9/10) Loading Connectivity"
        self.loadConnectivity()
        print "(10/10) Loading Author Structure"
        self.loadAuthorStructure()

    def loadUsers(self):
        if (self.loadedUsers):
            return

        currFile = open(usersFile, 'r')
        for line in currFile:
            line = line[:-1]
            row = line.split("||")
            u = createUserFromCSV(row)
            if u.isReviewer:
                self.reviewers[u.id] = u
            self.users[u.id] = u

        self.loadedUsers = True

        if (self.loadedPapers):
            self.loadUsersPapersJoin()
        if (self.loadedPastPapers):
            self.loadPastPapersUsersJoin()

    def loadPapers(self):
        if (self.loadedPapers):
            return

        currFile = open(papersFile, 'r')
        for line in currFile:
            line = line[:-1]
            row = line.split("||")
            p = createPaperFromCSV(row)
            self.papers[p.id] = p

        self.loadedPapers = True

        if (self.loadedUsers):
            self.loadUsersPapersJoin()

    def loadPastPapers(self):
        if (self.loadedPastPapers):
            return

        self.processPastPaperFile(pastPapersConferencesFile, True)
        self.processPastPaperFile(pastPapersJournalsFile, False)

        if (self.loadedUsers):
            self.loadPastPapersUsersJoin()

        self.loadedPastPapers = True

    def processPastPaperFile(self, filename, isConference):
        currFile = open(filename, 'r')
        for line in currFile:
            line = line[:-1]
            row = line.split("||")
            p = createPastPaperFromCSV(row, isConference)
            self.pastPapers[p.id] = p

    def loadUsersPapersJoin(self):
        assert self.loadedPapers
        assert self.loadedUsers

        self.loadBids()

        currFile = open(usersPapersJoinFile, 'r')
        for line in currFile:
            line = line[:-1]
            row = line.split("||")
            paperId = int(row[0])
            userId = int(row[1])
            isPrimaryAuthor = (row[2] == "True")

            assert userId in self.users
            u = self.users[userId]
            assert paperId in self.papers
            p = self.papers[paperId]

            u.addPaper(p, isPrimaryAuthor)

            p.authors.append(u)
            if isPrimaryAuthor:
                p.primaryAuthor = u

    def loadBids(self):
        assert self.loadedPapers
        assert self.loadedUsers

        currFile = open(bidsFile, 'r')
        for line in currFile:
            line = line[:-1]
            row = line.split("\t")
            userId = int(row[0])
            paperId = int(row[1])
            bid = int(row[3])

            if paperId in self.papers:
                assert userId in self.reviewers
                p = self.papers[paperId]
                u = self.users[userId]

                u.bids[paperId] = bid
                p.bids[userId] = bid

    def loadPastPapersUsersJoin(self):
        currFile = open(pastPapersUsersJoinFile, 'r')
        for line in currFile:
            line = line[:-1]
            row = line.split("||")
            userId = int(row[0])
            pastPaperIdList = row[1].replace("[", "")\
                                    .replace("]", "")\
                                    .replace("'", "")\
                                    .split(", ")

            assert userId in self.users
            u = self.users[userId]

            for pId in pastPaperIdList:
                pId = int(pId)
                assert pId in self.pastPapers
                p = self.pastPapers[pId]

                u.pastPapers.append(p)

    def loadSubjectAreas(self):
        if self.loadedSubjectAreas:
            return
        assert self.loadedUsers

        currFile = open(subjectAreasFiles, 'r')
        for line in currFile:
            line = line[:-1]
            row = line.split("\t")
            userId = int(row[0])
            generalSubjectArea = row[1]
            specificSubjectArea = row[2]
            isPrimary = row[3][:-1] == "Primary"

            assert userId in self.reviewers
            u = self.reviewers[userId]

            u.generalSubjectAreas.add(generalSubjectArea)
            u.specificSubjectAreas.append(specificSubjectArea)

            if isPrimary:
                u.primaryGeneralSubjectArea = generalSubjectArea
                u.primarySpecificSubjectArea = specificSubjectArea

        self.loadedSubjectAreas = True

    def loadReviews(self):
        if self.loadedReviews:
            return
        assert self.loadedUsers
        assert self.loadedPapers

        currFile = open(reviewsFile, 'r')
        for line in currFile:
            line = line[:-1]
            row = line.split("\t")
            r = createReviewFromCSV(row)

            if r.userId == -1:
                print r.ratings["comments"]
                print r.ratings["strengths"]

            self.reviewsSharedCode(r)

            self.reviews[r.id] = r
            r.user.reviews.append(r)
            r.paper.reviews.append(r)

        currFile = open(metaReviewsFile, 'r')
        for line in currFile:
            line = line[:-1]
            row = line.split("\t")
            r = createMetaReviewFromCSV(row)

            self.reviewsSharedCode(r)

            self.metaReviews[r.id] = r
            r.user.metaReviews.append(r)
            r.paper.metaReviews.append(r)

        self.loadedReviews = True

        currFile = open(timeFile, 'r')
        for line in currFile:
            line = line[:-1]
            row = line.split('\t')
            self.reviews[int(row[0])*10000 + int(row[1])].time =\
                datetime.datetime.strptime(row[2].strip(), "%m/%d/%Y %I:%M:%S %p")


    def reviewsSharedCode(self, r):
        assert r.userId in self.reviewers
        assert r.paperId in self.papers

        r.user = self.reviewers[r.userId]
        r.paper = self.papers[r.paperId]
        del r.userId
        del r.paperId

    def loadAcceptance(self):
        assert self.loadedPapers

        currFile = open(acceptanceFile, 'r')
        for line in currFile:
            line = line[:-1]

            paperId = int(line)

            assert paperId in self.papers
            self.papers[paperId].accepted = True

    def loadDistance(self):
        assert self.loadedUsers
        currFile = open(distanceFile, 'r')
        for line in currFile:
            tokens = line[:-1].split('||')
            tokens = map(int, tokens)

            userId = tokens[0]

            assert userId in self.users
            user = self.users[userId]

            i = 1
            length = len(tokens)
            while i < length:
                otherId = tokens[i]
                i += 1
                dist = tokens[i]
                i += 1

                assert otherId in self.users
                user.distances[otherId] = dist
        currFile.close()

    def loadAbstracts(self):
        assert self.loadedPastPapers
        for subdir, dirs, files in os.walk(abstractsFolder):
            for f in files:
                currFile = open(abstractsFolder + "/" + f, 'r')
                for line in currFile:
                    tokens = line[:-1].split('||')
                    paperId = int(tokens[0])
                    assert paperId in self.pastPapers
                    self.pastPapers[paperId].abstract = tokens[1]

    def loadConnectivity(self):
        assert self.loadedUsers
        assert self.loadedPapers
        currFile = open(centralitiesFile, 'r')
        for line in currFile.read().splitlines():
            tokens = line.split(',')
            user = self.users[int(tokens[0])]
            user.pageRank = float(tokens[1])
            user.degCenter = float(tokens[3])
        currFile.close()
        currFile = open(connectivityFile, 'r')
        for line in currFile.read().splitlines():
            tokens = line.split(',')
            user = self.users[int(tokens[0])]
            user.numSiblings = int(tokens[1])
            user.numCousins = int(tokens[2])
            user.connectivity = user.numCousins * 1.0 / 1439708
        currFile.close()
        for id, paper in self.papers.iteritems():
            paper.maxConnectivity = max(a.connectivity for a in paper.authors)
            paper.maxPageRank = max(a.pageRank for a in paper.authors)
            paper.maxDegCenter = max(a.degCenter for a in paper.authors)

        # for line in currFile:
        #     tokens = line[:-1].split(',')
        #     self.users[int(tokens[0])].pageRank = float(tokens[1])
        # for id,paper in self.papers.iteritems():
        #     connectivities = [a.pageRank for a in paper.authors]
        #     paper.avgConnectivity = sum(connectivities)/len(connectivities)
        #     paper.maxConnectivity = max(connectivities)

    def loadClassifierAccuracy(self):
        assert self.loadedPapers
        assert self.loadedReviews

        for id, paper in self.papers.iteritems():
            self.papers[id].classifierAccReviews = -1

        def processReviewAccuracyByPaper(id, acc):
            self.papers[id].classifierAccReviews = acc

        def processReviewAccuracyByReviewAccept(id, acc):
            self.reviews[id].classifierAccAccept = acc

        def processReviewAccuracyByReviewRating(id, acc):
            self.reviews[id].classifierAccRating = acc

        def processAbstractAccuracyByPaper(id, acc):
            self.papers[id].classifierAccAbstract = acc

            if not self.papers[id].accepted:
                self.papers[id].classifierProbAbstract = 1 - acc
            else:
                self.papers[id].classifierProbAbstract = acc

        def processFile(filename, func):
            f = open(filename, 'r')

            for line in f:
                tokens = line[:-1].split(',')
                func(int(tokens[0]), float(tokens[1]))

        processFile(
            "analysis/iteration5/reviewAccuracyByPaper.csv",
            processReviewAccuracyByPaper)

        processFile(
            "analysis/iteration5/reviewAccuracyByReview.csv",
            processReviewAccuracyByReviewAccept)

        processFile(
            "analysis/iteration5/reviewAccuracyRating.csv",
            processReviewAccuracyByReviewRating)

        processFile(
            "analysis/iteration5/abstractAccuracyByPaper_PCA.csv",
            processAbstractAccuracyByPaper)


    def loadAuthorStructure(self):
        assert self.loadedPapers
        f = open(structureFile, "r")
        lines = f.read().splitlines()
        i = 0
        while i < len(lines):
            tokens = lines[i].split(' ')
            id = int(tokens[0])
            paper = self.papers[id]
            paper.noDBLP = int(tokens[1])
            paper.numCC = int(tokens[2])
            paper.numConn = int(tokens[3])
            paper.density = float(tokens[4])
            paper.avgDist = float(tokens[5])
            components = []
            for j in range(i+1, i+1+paper.numCC):
                tokens = lines[j].split(' ')
                for k in range(int(tokens[1])):
                    components.append(int(tokens[0]))
            if len(components) > 0:
                paper.avgSize = sum(components)*1.0/len(components)
                paper.maxSize = max(components)
            i += paper.numCC + 1
        f.close()

    def loadLikes(self):
        assert self.loadedPapers
        f = open(likesFile, "r")
        lines = f.read().splitlines()
        for line in lines:
            tokens = line.split('||')
            id = int(tokens[0])
            if id in self.papers:
                paper = self.papers[id]
                paper.likes = int(tokens[1])
        f.close()
