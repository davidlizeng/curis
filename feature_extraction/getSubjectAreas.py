from dataLoader import DataLoader

loader = DataLoader()
loader.loadAll()

fileobj = open("csv/subjectAreaDump.csv", 'w')

for id, paper in loader.papers.iteritems():
    if paper.accepted:
        fileobj.write("%s|%d|%s" % (
            paper.primarySpecificSubjectArea, id, paper.title))
        for subj in paper.specificSubjectAreas:
            fileobj.write("|" + subj)
        fileobj.write("\n")
fileobj.close()
