from feature_extraction.dataLoader import DataLoader

loader = DataLoader()
loader.loadAll()

numAbstracts = 0
for id, paper in loader.pastPapers.iteritems():
    if len(paper.abstract) > 3:
        numAbstracts += 1

print numAbstracts * 1.0 / len(loader.pastPapers)
