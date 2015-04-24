import urllib2
import xml.etree.ElementTree as et
import codecs
import sys
import time
import threading
import logging

##URLS
urlBase = 'http://dblp.uni-trier.de/'
urlCoauthors = urlBase + 'pers/xc/{0}'

usersFile = codecs.open('csv/manualChanges', 'r', 'utf-8')
usersLines = usersFile.read().splitlines()
# logging.getLogger().setLevel(10)
# logging.basicConfig(level=logging.DEBUG,
#                     format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
users = {}

# class Countdown:
#     def __init__(self, value):
#         self.value = value
#         self.lock = threading.Lock()

#     def tick(self):
#         self.lock.acquire()
#         if self.value > 0:
#             value = self.value
#             self.value = self.value - 1
#         else:
#             self.value = 0
#             value = 0
#         self.lock.release()
#         return value


def getCoauthors(lines, users):
    for line in lines:
        time.sleep(1)
        tokens = line.split('||')
        urlpt = tokens[2]
        coauthors = []
        if urlpt != '':
            url = urlCoauthors.format(urlpt)
            try:
                response = urllib2.urlopen(url).read()
                root = et.fromstring(response)
            except:
                time.sleep(60)
                logging.debug('Error getting response for ' + str(urlpt) + ' giving up...')
            authors = root.findall('*')
            for author in authors:
                key = author.attrib['urlpt'].encode('utf-8')
                count = int(author.attrib['count'])
                name = author.text.encode('utf-8')
                coauthors.append((key, name, count))
        users[urlpt] = coauthors

# counter = Countdown(len(usersLines))
# for i in range(1):
#     t = threading.Thread(target=getCoauthors, args=(usersLines, users, counter,))
#     t.start()


def writeCsv(lines, users):
    idmap = {}
    for line in lines:
        tokens = line.split('||')
        idmap[tokens[2]] = tokens[0]
    outfile = codecs.open('csv/dblpcoauthors.csv', 'a', 'utf-8')
    for user in users:
        for coauthor in users[user]:
            tokens = [idmap[user], coauthor[0], coauthor[1].decode('utf-8'), str(coauthor[2])]
            outfile.write('||'.join(tokens) + '\n')
    outfile.close()
