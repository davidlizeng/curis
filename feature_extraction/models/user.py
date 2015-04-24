from sets import Set


class User(object):

    def __init__(self):
        #list of papers written by author (Paper)
        self.papers = []
        #list of papers in which author was the primary author (Paper)
        #is subset of papers
        self.papersPrimary = []
        #list of past papers written by author (PastPaper)
        self.pastPapers = []
        #list of coauthors on kdd submission (User)
        self.coAuthors = []
        #dict from other user id's to distance from author
        #only keep track of authors within a distance of 6
        self.distances = {}

        self.isReviewer = False
        self.tfVector = None
        self.numSiblings = 0
        self.numCousins = 0
        self.connectivity = 0
        self.pageRank = 0
        self.degCenter = 0
        self.topPastPapers = 0
        self.topKDDPast = 0
        self.topNIPSPast = 0
        self.topSIGIRPast = 0
        self.topSIGMODPast = 0
        self.topICMLPast = 0
        self.topICDEPast = 0
        self.topICDMPast = 0

    def addPaper(self, paper, isPrimary):
        if isPrimary:
            self.papersPrimary.append(paper)
        self.papers.append(paper)


class Reviewer(User):

    def __init__(self):
        super(Reviewer, self).__init__()
        #list of reviews (Review)
        self.reviews = []
        #list of metaReviews
        self.metaReviews = []

        self.isReviewer = True
        #PaperId (int) -> Bid Value (int)
        self.bids = {}
        #set of general subject areas
        self.generalSubjectAreas = Set()
        #list of specific subject areas
        self.specificSubjectAreas = []

        #primary subject areas
        self.primaryGeneralSubjectArea = None
        self.primarySpecificSubjectArea = None

#takes in row of dblpusers.csv (see csv/README)
def createUserFromCSV(row):
    u = None
    if (checkReviewer(row)):
        u = Reviewer()

        #chair?
        u.isChair = getYesNo(row[6])
        #associateChair?
        u.isAssociateChair = getYesNo(row[7])
        #metaReviewer?
        u.isMetaReviewer = getYesNo(row[8])
        #regularReviewer?
        u.isRegularReviewer = getYesNo(row[9])
        #externalReviewer?
        u.isExternalReviewer = getYesNo(row[10])
    else:
        u = User()

    #userid
    u.id = int(row[0])
    #dblp_name
    u.name = row[1]
    #dblp_key
    u.dblpKey = row[2]
    #email address
    u.email = row[3]
    #affiliation
    u.affiliation = row[4]
    #submitPaper
    u.submittedPapers = getYesNo(row[5])
    #country
    u.country = row[11]
    #academic/industry
    u.isAcademic = row[12] == "Academic"

    return u


def checkReviewer(row):
    return "Yes" in row[6:]


def getYesNo(field):
    return field == "Yes"
