# -*- encoding: utf-8 -*-
import urllib
import codecs
import xml.etree.ElementTree as et

infile = codecs.open('users.csv', 'r', 'utf-8')
outfile = codecs.open('privelegedusers.csv', 'w', 'utf-8')
lines = infile.read().splitlines()

def has_status(status):
  return (status[0] or status[1] or status[2] or status[3] or status[4])

for line in lines:
  tokens = line.split('||')
  status = ''.join(tokens[7:12])
  if 'Yes' in status:
    outfile.write(line + '\n')