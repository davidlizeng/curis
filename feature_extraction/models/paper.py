from sets import Set


class Paper(object):
    def __init__(self):
        #list of authors of paper (User)
        self.authors = []
        self.primaryAuthor = None

        self.primaryGeneralSubjectArea = None
        self.primarySpecificSubjectArea = None
        self.generalSubjectAreas = Set()
        self.specificSubjectAreas = []

        #dictionary from user id -> bid number
        self.bids = {}

        self.reviews = []
        self.metaReviews = []

        #until set otherwise
        self.accepted = False
        self.tfVector = None
        self.abstract = ""
        self.likes = 0


#takes in row of papers.csv (see csv/README)
def createPaperFromCSV(row):

    p = Paper()

    #paperid
    p.id = int(row[0])
    #title
    p.title = row[1]
    #Research/Industry
    #abstract
    p.abstract = row[3]
    #subject areas
    processSubjectAreas(p, row[4])
    #conflitct names
    #keywords
    p.keywords = row[6]
    #student
    p.isStudent = row[7] == "Yes"

    return p


def processSubjectAreas(p, subjectAreas):
    subjectList = subjectAreas.split("; ")

    for s in subjectList:
        primary = False
        if '*' in s:
            primary = True
            s = s.replace("*", "")
        p.generalSubjectAreas.add(s.split("\\")[0])
        p.specificSubjectAreas.append(s)
        if primary:
            p.primaryGeneralSubjectArea = s.split("\\")[0]
            p.primarySpecificSubjectArea = s
