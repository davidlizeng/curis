# -*- encoding: utf-8 -*-
import urllib
import xml.etree.ElementTree as et
import codecs
import sys
import time

urlBase = 'http://dblp.uni-trier.de/'
urlPerson = urlBase + 'pers/xk/{0}'
urlCoauthors = urlBase + 'pers/xc/{0}'
urlPaper = urlBase + 'rec/bibtex/{0}.xml'
papersFile = codecs.open('csv/dblppapers.csv', 'r', 'utf-8')
papersLines = papersFile.read().splitlines()
finished = set()
joursFile = codecs.open('csv/dblpjours.csv', 'r', 'utf-8')
confsFile = codecs.open('csv/dblpconfs.csv', 'r', 'utf-8')
joursLines = joursFile.read().splitlines()
confsLines = confsFile.read().splitlines()
for line in joursLines:
  tokens = line.split('||')
  finished.add(tokens[0])
for line in confsLines:
  tokens = line.split('||')
  finished.add(tokens[0])
joursFile.close()
confsFile.close()

joursFile = codecs.open('csv/dblpjours.csv', 'a', 'utf-8')
confsFile = codecs.open('csv/dblpconfs.csv', 'a', 'utf-8')
confFields = ['pages','year','booktitle','ee','crossref','url']
jourFields = ['pages','year','volume','journal','number','ee','crossref','url']

def getAuthors(root):
  authors = []
  for author in root.findall('author'):
    authors.append(author.text)
  return authors

def getTitle(root):
  title = root.find('title')
  if title == None:
    return ''
  if title.text != None:
    return title.text
  text = ''
  for child in title.findall('*'):
    if child.text != None:
      text = text + child.text
    if child.tail != None:
      text = text + child.tail
  return text

def getText(root, fieldTag):
  field = root.find(fieldTag)
  if field != None and field.text != None:
    return field.text
  return ''

def getXML(key):
  while True:
    try:
      response = urllib.urlopen(urlPaper.format(key)).read()
      root = et.fromstring(response).find('*')
      break
    except:
      print 'Error getting response for',key,'retrying...'
      sys.stdout.flush()

  print 'Got response for',key
  sys.stdout.flush()
  return root

count = 0
for line in papersLines:
  count = count + 1
  if count % 100 == 0:
    print '***********************************************', count
    sys.stdout.flush()
  tokens = line.split('||')
  if tokens[0] not in finished:
    time.sleep(0.5)
    id = int(tokens[0])
    key = tokens[1]
    root = getXML(key)
    if key[0:4] == 'jour':
      fields = jourFields
      outfile = joursFile
    else:
      fields = confFields
      outfile = confsFile
    outfile.write(str(id) + '||' + key + '||' + str(getAuthors(root)) + '||' + getTitle(root))
    for field in fields:
      outfile.write('||' + getText(root, field))
    outfile.write('\n')

papersFile.close()
joursFile.close()
confsFile.close()
