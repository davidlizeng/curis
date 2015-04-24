import urllib
import codecs
import sys
import xml.etree.ElementTree as et

mfiles = []
mfiles.append(codecs.open('../csv/matched.csv', 'r', 'utf-8'))
mfiles.append(codecs.open('../csv/goodnames.csv', 'r', 'utf-8'))
mfiles.append(codecs.open('../csv/exactmatches.csv', 'r', 'utf-8'))
mfiles.append(codecs.open('../csv/nonames2.csv', 'r', 'utf-8'))
mfiles.append(codecs.open('../csv/multinames3.csv', 'r', 'utf-8'))
nfiles = []
nfiles.append(codecs.open('../csv/mnonames.csv', 'r', 'utf-8'))
nfiles.append(codecs.open('../csv/reviewers_no_dblp.csv', 'r', 'utf-8'))
nfiles.append(codecs.open('../csv/nonames3.csv', 'r', 'utf-8'))

finalfile = codecs.open('../csv/dblpusers.csv', 'w', 'utf-8')

mlines = []
for f in mfiles:
  mlines.append(f.read().splitlines())

nlines = []
for f in nfiles:
  nlines.append(f.read().splitlines())

users = {}
for f in mlines:
  for line in f:
    tokens = line.split('||')
    if int(tokens[0]) in users:
      print "Repeated user? This shouldnt happen"
    else:
      users[int(tokens[0])] = line

for f in nlines:
  for line in f:
    tokens = line.split('||')
    if int(tokens[0]) in users:
      print "Repeated user? This shouldnt happen"
    else:
      name = tokens[1] + ' '
      if tokens[2] != '':
        name = name + tokens[2] + ' '
      name = name + tokens[3]
      users[int(tokens[0])] = tokens[0] + '||' + name + '||||' + '||'.join(tokens[4:]) 

sorted_ids = sorted(users)
for id in sorted_ids:
  finalfile.write(users[id] + '\n')

finalfile.close()

for f in mfiles:
  f.close()

for f in nfiles:
  f.close()

s = set()
usersfile = codecs.open('../csv/users.csv', 'r', 'utf-8')
dblpfile = codecs.open('../csv/dblpusers.csv', 'r', 'utf-8')
lines = dblpfile.read().splitlines()
for line in lines:
  tokens = line.split('||')
  s.add(tokens[0])
lines = usersfile.read().splitlines()
for line in lines:
  tokens = line.split('||')
  if tokens[0] not in s:
    print "Missing user", line

usersfile.close()
dblpfile.close() 
