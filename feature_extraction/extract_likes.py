import json
from pprint import pprint
from feature_extraction.dataLoader import DataLoader
from collections import defaultdict

# loader = DataLoader()
# loader.loadUsers()
# loader.loadPapers()
# loader.loadPastPapers()
# loader.loadReviews()
# loader.loadAcceptance()

likeFile = open('conf_data/confer-anonymized_data_dump.json', 'r')
likeData = json.load(likeFile)['data']

#research paper ids are just frp + paper id. e.g. paper 1007 and 657 have ids
# frp1007 and frp0657, respectively
paperFile = open('conf_data/kdd-papers.json', 'r')
paperData = json.load(paperFile)

# for id in paperData:
#   if 'frp' in id:
#     paperId = int(id[3:])
#     paper = loader.papers[paperId]
#     if not paper.accepted:
#       print 'unknown paper', id

# accepted = sum([paper.accepted for  id, paper in loader.papers.iteritems()])

likeCounts = defaultdict(int)
for obj in likeData:
  for id in obj['likes']:
    likeCounts[id] += 1

paperLikes = open('csv/likes.csv', 'w')
for id, likes in likeCounts.iteritems():
  if 'frp' in id:
    paperLikes.write(id[3:] + '||' + str(likes) + '\n')
paperLikes.close()
