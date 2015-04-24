class Review(object):
    nextId = 0

    def __init__(self):
        self.paper = None
        self.user = None

        self.ratings = {}
        self.overallRating = None

    def getReviewText(self):
        return "%s %s %s" % (
            self.ratings["strengths"],
            self.ratings["weaknesses"],
            self.ratings["comments"])


class MetaReview(object):
    nextId = 0

    def __init__(self):
        self.paper = None
        self.user = None

        self.ratings = {}
        self.overallRating = None
        self.overallAssessment = None


#takes in row of ReviewsRevised.tsv (see csv/reviews/README_Reviews.txt)
def createReviewFromCSV(row):

    r = Review()
    r.paperId = int(row[0])  # to be deleted
    r.userId = int(row[1])  # to be deleted
    r.id = r.paperId*10000 + r.userId
    r.confidence = int(row[2])
    r.ratings["novelty"] = int(row[3])
    r.ratings["technicalDevelopment"] = int(row[4])
    r.ratings["empirical"] = int(row[5])
    r.ratings["repeatability"] = row[6]
    r.ratings["presentation"] = int(row[7])
    r.topicCategory = row[8]
    r.overallRating = int(row[9])  # listed as overall recommendation
    r.ratings["strengths"] = row[10]
    r.ratings["weaknesses"] = row[11]
    r.ratings["comments"] = row[12]
    #r.ratings["grammaticalErrors"] = row[13]
    r.ratings["confidentialComments"] = row[14]
    #r.furtherReview = row[15]
    #r.furtherConsultation = row[16]
    r.externalReviewer = row[17]
    r.bestPaperSeen = row[18] == "Yes"
    r.time = None

    return r


#takes in row of MetaReviewerRevised.tsv (see csv/reviews/README_Reviews.txt)
def createMetaReviewFromCSV(row):

    r = MetaReview()
    r.paperId = int(row[0])  # to be deleted
    r.userId = int(row[1])  # to be deleted
    r.id = r.paperId*10000 + r.userId
    r.percentile = row[2]
    r.overallRating = int(row[3])
    r.overallAssessment = row[4]
    r.ratings["confidentialComments"] = row[5]
    r.bestPaperNominate = int(row[6]) == 1
    r.condAccept = row[7]
    r.condAcceptConditions = row[8]

    return r
