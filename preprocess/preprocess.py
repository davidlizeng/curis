#infile = open('users.csv', 'r')
#outfile = open('names.txt', 'w')
#lines = infile.readlines()
#for line in lines:
#  tokens = line.split(',')
#  outfile.write(tokens[0].replace('-',' ').strip() + ' ' + tokens[2].replace('-',' ').strip() + ' ' + tokens[1].replace('-',' ').strip() + '\n')
#infile.close()
#outfile.close()

import codecs
import csv
usersfile = open('users.csv', 'r')
papersfile = open('papers.csv', 'r')

def unicode_csv_reader(utf8_data):
  csv_reader = csv.reader(utf8_data)
  for row in csv_reader:
    yield [unicode(cell, 'utf-8') for cell in row]

usersreader = unicode_csv_reader(usersfile)
papersreader = unicode_csv_reader(papersfile)

#ID,FirstName,MiddleInitial,LastName,Email,Organization,IsAssociateChair,IsReviewer,IsExternalReviewer,IsMetaReviewer,IsSubmissionOwner,IsChair
#Paper ID,Paper Title,Track Name,Abstract,Author Names,Author Emails,Subject Areas,Conflict Reasons,Free text keywords,student?
papers = []
for row in papersreader:
  emails = row[5].replace(' ','').lower().split(';')
  papers.append({'id': int(row[0]), 'emails': emails, 'users': [0]*len(emails)})

def create_status(c, ac, mr, r, er):
  return [c == u'Yes', ac == u'Yes', mr == u'Yes', r == u'Yes', er == u'Yes']

def has_status(status):
  return (status[0] or status[1] or status[2] or status[3] or status[4])

def num_status(status):
  return status[0] + status[1] + status[2] + status[3] + status[4]

users = []
for row in usersreader:
  users.append({'id': int(row[0]), 'email': row[4].strip().lower(), 'papers': [], 'owner': row[10] == u'Yes', 'status': create_status(row[11], row[6], row[9], row[7], row[8])})

for user in users:
  for paper in papers:
    for i in range(0,len(paper['emails'])):
      if paper['emails'][i] == user['email']:
        user['papers'].append(paper['id'])
        paper['users'][i] = user['id']

usersfile.close()
papersfile.close()
usersfile = open('users.csv', 'r')
papersfile = open('papers.csv', 'r')
usersreader = unicode_csv_reader(usersfile)
papersreader = unicode_csv_reader(papersfile)

newusersfile = codecs.open('newusers.csv', 'w', 'utf-8')
for i in range(0, len(users)):
  row = usersreader.next()
  if int(row[0]) != users[i]['id']:
    print 'WTF'
  if len(users[i]['papers']) != 0 or has_status(users[i]['status']):
    newusersfile.write(row[0] + '||' + row[1] + '||' + row[2] + '||' + row[3] + '||' + row[4] + '||' + row[5] + '||' + row[10] + '||' + row[11] + '||' + row[6] + '||' + row[9] + '||' + row[7] + '||' + row[8] + '\n')

newpapersfile = codecs.open('newpapers.csv', 'w', 'utf-8')
for i in range(0, len(papers)):
  row = papersreader.next()
  if int(row[0]) != papers[i]['id']:
    print 'WTF'
  newpapersfile.write(row[0] + '||' + row[1] + '||' + row[2] + '||' + row[3] + '||' + row[6] + '||' + row[7] + '||' + row[8] + '||' + row[9] + '\n')

papersusersjoinfile = open('papersusers.csv', 'w')
for paper in papers:
  for i in range(0,len(paper['users'])):
    papersusersjoinfile.write('{0}||{1}||{2}\n'.format(paper['id'],paper['users'][i],i==0))

