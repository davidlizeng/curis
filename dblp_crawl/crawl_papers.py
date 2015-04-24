import urllib
import xml.etree.ElementTree as et
import codecs
import sys
import time

##URLS
urlBase = 'http://dblp.uni-trier.de/'
urlPerson = urlBase + 'pers/xk/{0}'
urlCoauthors = urlBase + 'pers/xc/{0}'
urlPaper = urlBase + 'rec/bibtex/{0}.xml'

def scrapeAllPapers():
  usersFile = codecs.open('../csv/dblpusers.csv', 'r', 'utf-8')
  usersLines = usersFile.read().splitlines()
  joinFile = codecs.open('../csv/dblpuserspapers.csv', 'w', 'utf-8')
  papersFile = codecs.open('../csv/dblppapers.csv', 'w', 'utf-8')

  papers = {}
  usersPapers = {}

  globalpapersid = 1

  for line in usersLines:
    time.sleep(0.5)
    tokens = line.split('||')
    urlpt = tokens[2]
    if urlpt != '':
      userid = int(tokens[0])
      usersPapers[userid] = []
      while True:
        try:
          response = urllib.urlopen(urlPerson.format(urlpt)).read()
          root = et.fromstring(response)
          break
        except:
          print 'Error getting response for',urlpt,'retrying...'
          sys.stdout.flush()

      print 'Got reponse for',urlpt
      sys.stdout.flush()

      for paper in root.findall('dblpkey'):
        if 'type' not in paper.attrib:
          key = paper.text
          if key not in papers:
            papers[key] = globalpapersid
            globalpapersid = globalpapersid + 1
          usersPapers[userid].append(papers[key])

  reverseMap = {}
  for key in papers:
    reverseMap[papers[key]] = key

  for id in sorted(reverseMap.keys()):
    papersFile.write(str(id) + '||' + reverseMap[id] + '\n')

  for id in sorted(usersPapers.keys()):
    joinFile.write(str(id) + '||' + str(usersPapers[id]) + '\n')

  usersFile.close()
  papersFile.close()
  joinFile.close()


def addPapers(filename):
  usersFile = codecs.open(filename, 'r', 'utf-8')
  usersLines = usersFile.read().splitlines()
  papersFile = codecs.open('csv/dblppapers.csv', 'r', 'utf-8')
  papersLines = papersFile.read().splitlines()
  papers = {}
  newpapers = {}
  usersPapers = {}
  for line in papersLines:
    tokens = line.split('||')
    papers[tokens[1]] = int(tokens[0])
  globalpapersid = max(papers.values()) + 1
  papersFile.close()
  for line in usersLines:
    time.sleep(0.5)
    tokens = line.split('||')
    urlpt = tokens[2]
    if urlpt != '':
      userid = int(tokens[0])
      usersPapers[userid] = []
      while True:
        try:
          response = urllib.urlopen(urlPerson.format(urlpt)).read()
          root = et.fromstring(response)
          break
        except:
          print 'Error getting response for',urlpt,'retrying...'
          sys.stdout.flush()

      print 'Got reponse for',urlpt
      sys.stdout.flush()

      for paper in root.findall('dblpkey'):
        if 'type' not in paper.attrib:
          key = paper.text
          if key not in papers:
            papers[key] = globalpapersid
            newpapers[key] = globalpapersid
            globalpapersid = globalpapersid + 1
          usersPapers[userid].append(papers[key])

  papersFile = codecs.open('csv/dblppapers.csv', 'a', 'utf-8')
  joinFile = codecs.open('csv/dblpuserspapers.csv', 'a', 'utf-8')
  reverseMap = {}
  for key in newpapers:
    reverseMap[newpapers[key]] = key
  for id in sorted(reverseMap.keys()):
    papersFile.write(str(id) + '||' + reverseMap[id] + '\n')
  for id in sorted(usersPapers.keys()):
    joinFile.write(str(id) + '||' + str(usersPapers[id]) + '\n')
