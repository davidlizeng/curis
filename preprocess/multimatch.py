# -*- encoding: utf-8 -*-
# Takes each name from users.csv and tries to query DBLP for an entry for the name. 
# Some queries may return with no entries, or multiple matching ones.
import urllib
import codecs
import sys
import xml.etree.ElementTree as et

infile = codecs.open('../csv/multinames.csv', 'r', 'utf-8')
goodfile = codecs.open('../csv/exactmatches.csv', 'w', 'utf-8')
badfile = codecs.open('../csv/multinames2.csv', 'w', 'utf-8')

lines = infile.read().splitlines()

i = 0
while i < len(lines):
  found = False
  tokens = lines[i].split('||')
  name = tokens[2] + ' '
  if tokens[3] != '':
    name = name + tokens[3] + ' '
  name = name + tokens[4]
  for j in range(1, int(tokens[0]) + 1):
    entry = lines[i+j].split('||')
    if name == entry[0]:
      goodfile.write(tokens[1] + '||' + lines[i+j] + '||' + '||'.join(tokens[5:]) + '\n')
      found = True
  if not found:
    for j in range(1, int(tokens[0]) + 1):
      entry = lines[i+j].split('||')
      if name.lower() == entry[0].lower():
        goodfile.write(tokens[1] + '||' + lines[i+j] + '||' + '||'.join(tokens[5:]) + '\n')
        found = True
  if not found:
    badfile.write(lines[i] + '\n')
    for j in range(1, int(tokens[0]) + 1):
      badfile.write(lines[i+j] + '\n')
  i = i + int(tokens[0]) + 1

infile.close()
goodfile.close()
badfile.close()