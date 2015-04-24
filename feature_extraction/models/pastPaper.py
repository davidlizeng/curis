class PastPaper(object):

    def __init__(self):
        self.abstract = ""
        self.tfVector = None


#takes in row of dblpcnfs or dblpjours (see csv/README)
def createPastPaperFromCSV(row, isConference):

    p = PastPaper()

    #past_paperid
    p.id = int(row[0])
    #dblp_paperKey
    p.dblpKey = row[1]
    #[dblp_name]
    p.authors = processCSVList(row[2])
    #title
    p.title = row[3]
    #pageNumber
    #year
    try:
        p.year = int(row[5])
    except ValueError:
        p.year = 2014

    if isConference:
        p.isConference = True
        #conferenceName
        p.name = row[6]
    else:
        p.isConference = False
        #volume
        #journalName
        p.name = row[7]

    #doi
    p.doi = row[-3]
    #crossref
    #dblp_url

    return p


def processCSVList(l):
    return l.replace("['", "").replace("']", "").split("', '")
