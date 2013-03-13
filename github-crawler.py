#!/usr/bin/env python

# Prakash Gamit <prakashgamit23@gmail.com>
# Indian Institute of Technology, Roorkee

from httplib import *
import sys

# global connection object
conn=''

def getPage(url):
    global conn
    conn.request('GET', url)

    response = conn.getresponse()

    if response.status == 200:
        return response.read()
    else:
        print 'Error retrieving page from github'
        return
# end getPage()


def main():
    global conn
    conn = HTTPSConnection('github.com')

    username = sys.argv[1]
    homepage = getPage('/' + username)
    followers = getPage('/' + username + '/followers')
    following = getPage('/' + username + '/following')
    starred = getPage('/' + username + '/starred')

    conn.close()

    # parse homepage
    print 'username:', username

    start = homepage.find('itemprop="name"')
    end = homepage[start:].find('<')
    print '--Name:', homepage[(start+16) : (start+end)]

    start = homepage.find('itemprop="worksFor"')
    end = homepage[start:].find('<')
    print '--Works for:', homepage[(start+20) : (start+end)]

    start = homepage.find('itemprop="homeLocation"')
    end = homepage[start:].find('<')
    print '--Home Location:', homepage[(start+25) : (start+end)]

    start = homepage.find('join-date')
    end = homepage[start:].find('<')
    print '--Joined on:', homepage[(start+11) : (start+end)]
