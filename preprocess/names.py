# -*- encoding: utf-8 -*-
# Takes each name from users.csv and tries to query DBLP for an entry for the name. 
# Some queries may return with no entries, or multiple matching ones.
import urllib
import codecs
import sys
import xml.etree.ElementTree as et

infile = codecs.open('../csv/unmatched.csv', 'r', 'utf-8')
goodfile = codecs.open('../csv/singlenames.csv', 'w', 'utf-8')
nonefile = codecs.open('../csv/nonames.csv', 'w', 'utf-8')
multifile = codecs.open('../csv/multinames.csv','w', 'utf-8')
url = 'http://dblp.uni-trier.de/search/author?xauthor={0}'

lines = infile.read().splitlines();
# sometimes the script just stops running due to a request timing out
# for now just have a count that allows us to restart the script halfway through
count = 0
for line in lines[count:]:
  # build a query parameter for the author out of first and last name
  # $ is placed after these tokens to denote we want exact matches
  param = ''
  tokens = line.split('||')
  param = tokens[1].replace('-','$') + '$' + tokens[3] + '$'
  param = urllib.quote(param.strip().encode('utf-8'))
  while True:
    try:
      response = urllib.urlopen(url.format(param)).read()
      break
    except:
      print 'Error getting response for',param,'retrying...'
  # xml response just has a bunch of children for all
  # dblp entries that match the query, i.e.
  # <authors>
  #   <author urlpt="c/Corcoran:Diarmuid">Diarmuid Corcoran</author>
  #   <author urlpt="e/Early:Diarmuid">Diarmuid Early</author>
  # </author>
  root = et.fromstring(response)
  authors = root.findall('*')
  num = len(authors)
  if num == 0:
    nonefile.write(line + '\n')
  elif num > 1:
    multifile.write(str(num) + '||' + line + '\n')
    for i in range(0, num):
      multifile.write(authors[i].text + '||' + authors[i].attrib['urlpt'] + '\n')
  else:
    goodfile.write(tokens[0] + '||' + authors[0].text + '||' + authors[0].attrib['urlpt'] + '||' + '||'.join(tokens[4:]) + '\n')
  count = count + 1
  if count%100 == 0:
    print count
    sys.stdout.flush() 
infile.close()
goodfile.close()
nonefile.close()
multifile.close()