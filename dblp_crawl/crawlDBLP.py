#! /usr/bin/python
import urllib
import xml.etree.ElementTree as et
import csv

##URLS
urlBase = 'http://dblp.uni-trier.de/'
urlPerson = urlBase + 'pers/xk/{0}'
urlPaper = urlBase + 'rec/bibtex/{0}.xml'

##globals
paperIdCounter = 1
paperAuthorCounter = 1

##File
paperFileWriter = csv.writer(open('papers.csv', 'wb'))
paperAuthorsFileWriter = csv.writer(open('paperAuthors.csv', 'wb'))

#reads names from file and passes into worker function
def readFile(worker):
	file = open('../goodnames20.txt','r')
	for line in file:
		#find authorid
		space = line.find(" ")
		authorId = int(line[:space])

		#find backslash index
		bslash = line.find("/")
		crawlPerson(authorId, line[bslash-1:])

#starts file crawl by pulling down dblp page for author
def crawlPerson(authorId, dblpName):
	personPage = urllib.urlopen(urlPerson.format(dblpName)).read();

	#XML Format
	#<dblpperson name="Wei-Feng Tung">
	#	<dblpkey type="person record">homepages/31/6220</dblpkey>
	#	<dblpkey>journals/isf/TungL13</dblpkey>
	#	<dblpkey>conf/icssi/HuangT13</dblpkey>
	#</dblpperson>
	root = et.fromstring(personPage)
	for key in root.findall('dblpkey'):
		print(key.text)
		bslash = key.text.find("/")
		paperType = key.text[:bslash]

		isJournal = True
		if (paperType != "homepages"):
			if (paperType == "conf"):
				isJournal = False
			processPaper(authorId, isJournal, key.text)

#gets text out of xml field in root (returns empty string if not there)
def getText(root, fieldTag):
	field = root.find(fieldTag)
	if(field != None):
		return field.text.encode('utf-8')
	return ''

#crawls paper and writes entry to file
#arguments: author id, boolean for whether a journal, key for dblp url
def processPaper(authorId, isJournal, dblpKey):
	global paperIdCounter, paperAuthorCounter

	connected = False;
	while not connected:
		try:
			paperPage = urllib.urlopen(urlPaper.format(dblpKey)).read()
			connected = True;
		except Exception:
			print("URL OPEN FAIL")
			pass
		
	root = et.fromstring(paperPage).find("*")

	paperRow = [paperIdCounter, authorId, dblpKey]

	fields = [
		"title",
		"pages",
		"year",
		"volume",
		"booktitle",
		"ee",
		"crossref" 
	]

	if (isJournal):
		fields[4] = "journal"

		paperRow.append("journal")
	else:
		paperRow.append("conference")
	
	for field in fields:
		paperRow.append(getText(root, field))

	paperFileWriter.writerow(paperRow)

	for author in root.findall('author'):
		authorRow = [paperAuthorCounter, paperIdCounter]
		authorRow.append(author.text.encode('utf-8'))
		paperAuthorsFileWriter.writerow(authorRow)
		paperAuthorCounter += 1

	paperIdCounter += 1
readFile(crawlPerson)