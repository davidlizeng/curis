# -*- encoding: utf-8 -*-
from urlparse import urlparse
import urllib2
import xml.etree.ElementTree as et
import codecs
import sys
import time
from utilities.timeout import timeout, TimeoutError

@timeout(60)
def openUrl(request):
    response = urllib2.urlopen(request)
    return response.geturl()


def resolveRedirect(url):
    time.sleep(0.5)
    realUrl = ''
    try:
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36')
        realUrl = openUrl(request)
    except TimeoutError:
        print 'Request for',url,'timed out'
        sys.stdout.flush()
    except KeyboardInterrupt:
        print 'Interrupted'
        sys.stdout.flush()
        raise Exception('Terminating...')
    except:
        print 'Unknown error for',url,'giving up...'
        sys.stdout.flush()
    return realUrl


def getHosts(filename, urlindex, hosts, start, end):
    infile = codecs.open(filename, 'r', 'utf-8')
    if 'jours' in filename:
        type = 'jours'
    else:
        type = 'confs'
    outfile = codecs.open('/lfs/local/0/dzeng0/' + type + str(start), 'w', 'utf-8')
    lines = infile.read().splitlines()
    count = 0
    for line in lines[start:end]:
        count = count + 1
        tokens = line.split('||')
        redirectUrl = resolveRedirect(tokens[urlindex])
        parsedUrl = urlparse(redirectUrl)
        host = parsedUrl.hostname
        outfile.write(tokens[0] + '||' + redirectUrl + '\n')
        outfile.flush()
        if host not in hosts:
            hosts[host] = {'count': 0, 'urls':[]}
        hosts[host]['count'] = hosts[host]['count'] + 1
        hosts[host]['urls'].append(redirectUrl)
        if count % 10 == 0:
            print filename,start,count
            sys.stdout.flush()
    outfile.close()

def retryHostsFromFile(filename, dblpfile, urlindex):
    infile = codecs.open(filename, 'r', 'utf-8')
    ids = set()
    lines = infile.read().splitlines()
    for line in lines:
        tokens = line.split('||')
        ids.add(tokens[0])
    infile.close()
    outfile = codecs.open(filename + '_hosts', 'a', 'utf-8')
    papersfile = codecs.open(dblpfile, 'r', 'utf-8')
    lines = papersfile.read().splitlines()
    count = 0
    for line in lines:
        tokens = line.split('||')
        count = count + 1
        if count % 1000 == 0:
            print '*********************',count
        if tokens[0] in ids:
            time.sleep(1.0)
            redirectUrl = resolveRedirect(tokens[urlindex])
            parsedUrl = urlparse(redirectUrl)
            host = parsedUrl.hostname
            outfile.write(tokens[0] + '||' + redirectUrl + '\n')
    outfile.close()


def hostStats(filename):
    infile = open(filename, 'r')
    lines = infile.read().splitlines()
    infile.close()
    hosts = {}
    for line in lines:
        tokens = line.split('||')
        url = urlparse(tokens[1])
        if url.hostname not in hosts:
            hosts[url.hostname] = 0
        hosts[url.hostname] = hosts[url.hostname] + 1
    return hosts

# if __name__ == '__main__':
#     hosts = {}
#     getHosts('csv/dblpjours.csv', 9, hosts, 0, 10000)
#     getHosts('csv/dblpjours.csv', 9, hosts, 10000, 20000)
#     getHosts('csv/dblpjours.csv', 9, hosts, 20000, 30000)
#     getHosts('csv/dblpjours.csv', 9, hosts, 30000, 40000)
#     getHosts('csv/dblpconfs.csv', 7, hosts, 0, 10000)
#     getHosts('csv/dblpconfs.csv', 7, hosts, 10000, 20000)
#     getHosts('csv/dblpconfs.csv', 7, hosts, 20000, 30000)
#     getHosts('csv/dblpconfs.csv', 7, hosts, 30000, 40000)
#     getHosts('csv/dblpconfs.csv', 7, hosts, 40000, 50000)
#     getHosts('csv/dblpconfs.csv', 7, hosts, 50000, 60000)
#     getHosts('csv/dblpconfs.csv', 7, hosts, 60000, 70000)
#     getHosts('csv/dblpconfs.csv', 7, hosts, 70000, 80000)
