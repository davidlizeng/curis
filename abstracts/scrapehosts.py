# -*- coding: utf-8 -*-
from urlparse import urlparse
import cookielib
import urllib2
import urllib
import xml.etree.ElementTree as et
import codecs
import sys
import time
import os
from utilities.timeout import timeout, TimeoutError
from BeautifulSoup import BeautifulSoup

def buildProxyUrl(url):
    proxy = 'http://myproxyhasswag.info/index.php?q='
    return proxy + urllib.quote_plus(url) + '&hl=3e5'

@timeout(60)
def getResponse(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36')
    response = urllib2.urlopen(request).read()
    return BeautifulSoup(response)

def sanitizeText(text):
    text = text.replace('\n', ' ')
    return text

def scrapeArXiv(url):
    proxyUrl = buildProxyUrl(url)
    soup = getResponse(proxyUrl)
    return sanitizeText(soup.find('blockquote').text)

def scrapeIEEE(url):
    soup = getResponse(url)
    return sanitizeText(soup.find('div', {'class': 'article'}).text)

def scrapeSpringer(url):
    soup = getResponse(url)
    return sanitizeText(soup.find('p', {'class': 'a-plus-plus'}).text)

def scrapeACM(url):
    soup = getResponse(url + '&preflayout=flat')
    return sanitizeText(soup.find('div', {'style': 'display:inline'}).text)

def scrapeComputer(url):
    soup = getResponse(url)
    return sanitizeText(soup.find('div', {'class': 'abs-articlesummary'}).text)

def scrapeWiley(url):
    soup = getResponse(url[:url.rindex(';')])
    return sanitizeText(soup.find('div', {'class': 'para'}).text)

def scrapeIEICE(url):
    soup = getResponse(url)
    return sanitizeText(soup.findAll('span', {'class': 'TEXT-BODY'})[-1].text)

def scrapeIOS(url):
    soup = getResponse(url)
    return sanitizeText(soup.find('div', {'class': 'abstract'}).text)

def scrapeBMC(url):
    soup = getResponse(url)
    return sanitizeText(soup.findAll('p', {'style': 'line-height:160%'})[0].text)

def scrapeOJS(url):
    soup = getResponse(url)
    return sanitizeText(soup.find('div', {'id': 'articleAbstract'}).text)

def scrapeOxford(url):
    soup = getResponse(url)
    return sanitizeText(soup.find('div', {'id': 'abstract-1'}).text)

@timeout(20)
def postScienceDirect(postUrl, origUrl):
    data = urllib.urlencode({'citation-type': 'ASCII', 'export': 'Export', 'format': 'cite-abs', 'zone': 'exportDropDown'})
    request = urllib2.Request(postUrl, data)
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36')
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    request.add_header('Referer', origUrl)
    response = urllib2.urlopen(request)
    return response.read()

def scrapeScienceDirect(url):
    soup = getResponse(url)
    form = soup.find('form', {'name':'exportCite'})
    for pairs in form.attrs:
        if pairs[0] == 'action':
            params = pairs[1]
    postUrl = 'http://www.sciencedirect.com' + params
    text = sanitizeText(postScienceDirect(postUrl, url))
    return text[text.index('Abstract: ') + 10 : ]


hostMap = { 'arxiv': {'host': 'arxiv.org', 'method': scrapeArXiv},
            'ieee': {'host': 'ieeexplore.ieee.org', 'method': scrapeIEEE},
            'acm': {'host': 'dl.acm.org', 'method': scrapeACM},
            'springer': {'host': 'link.springer.com', 'method': scrapeSpringer},
            'sciencedirect': {'host': 'www.sciencedirect.com', 'method': scrapeScienceDirect},
            'computer': {'host': 'www.computer.org', 'method': scrapeComputer},
            'wiley': {'host': 'onlinelibrary.wiley.com', 'method': scrapeWiley},
            'ieice': {'host': 'search.ieice.org', 'method': scrapeIEICE},
            'ios': {'host': 'iospress.metapress.com', 'method': scrapeIOS},
            'bmc': {'host': 'www.biomedcentral.com', 'method': scrapeBMC},
            'ojs': {'host': 'ojs.academypublisher.com', 'method': scrapeOJS},
            'oxford': {'host': 'bioinformatics.oxfordjournals.org', 'method': scrapeOxford} }

# no links: tandfonline, worldscientific, epubs.siam
# pdfs: jmlr (some are .html), anthology.aclweb
# loads abs later: inderscience
# worth trying: bioinformatics.oxfordjournals
directory = '/lfs/local/0/dzeng0/'

def scrapeHost(filenames, hostname, mode):
    hostname = hostname.lower()
    papersToLinks = {}
    for filename in filenames:
        infile = open(directory + filename, 'r')
        #infile = open(filename, 'r')
        lines = infile.read().splitlines()
        for line in lines:
            tokens = line.split('||')
            papersToLinks[tokens[0]] = tokens[1]
        infile.close()
    if mode == None:
        outfile = open(directory + 'abs_' + hostname, 'w')
        failfile = open(directory + 'fail_' + hostname, 'w')
        #outfile = open('abs_' + hostname, 'w')
    elif mode == 'fail':
        fileCount = 1
        while os.path.isfile(directory + 'abs_' + hostname + '_' + str(fileCount)):
            fileCount = fileCount + 1
        outfile = open(directory + 'abs_' + hostname + '_' + str(fileCount), 'w')
        failfile = open(directory + 'fail_' + hostname + '_' + str(fileCount), 'w')
    count = 0
    errorCount = 0
    for paper in papersToLinks:
        url = urlparse(papersToLinks[paper])
        host = url.hostname
        if host == hostMap[hostname]['host']:
            try:
                count = count + 1
                if count % 10 == 0:
                    print hostname, count
                    sys.stdout.flush()
                #if 'cookiedetectresponse' not in papersToLinks[paper]:
                time.sleep(1.0)
                abstract = hostMap[hostname]['method'](papersToLinks[paper])
                if type(abstract) == unicode:
                    abstract = abstract.encode('utf-8')
                outfile.write(paper + '||' + abstract + '\n')
            except KeyboardInterrupt:
                print 'Interrupted'
                break
            except:
                print 'Error for', url.geturl()
                errorCount = errorCount + 1
                failfile.write(paper + '||' + url.geturl() + '\n')
    outfile.close()
    failfile.close()
    print 'Total abstracts scraped from host', hostname, count
    print 'Total links from host that errored out', errorCount


if __name__ == '__main__':
    if sys.argv[1] == 'fail':
        scrapeHost([sys.argv[2]], sys.argv[3], 'fail')
    else:
        scrapeHost(['jours', 'confs'], sys.argv[1], None)




# @timeout(10)
# def getResponseWCookies(url, cookies):
#     print url
#     print "***************** BEFORE"
#     for cookie in cookies:
#         print cookie.name, cookie.value
#     request = urllib2.Request(url)
#     request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36')
#     cookies.add_cookie_header(request)
#     response = urllib2.urlopen(request)
#     cookies.extract_cookies(response, request)
#     print "***************** AFTER"
#     for cookie in cookies:
#         print cookie.name, cookie.value

#     print response.getcode()
#     print response.geturl()
#     return BeautifulSoup(response.read())
