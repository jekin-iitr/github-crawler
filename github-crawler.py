#!/usr/bin/env python

# Prakash Gamit <prakashgamit23@gmail.com>
# Indian Institute of Technology, Roorkee

from httplib import *
import sys

def getPage(url):
    conn = HTTPSConnection('github.com')
    conn.request('GET', url)

    response = conn.getresponse()

    conn.close()

    if response.status == 200:
        return response.read()
    else:
        print 'Error retrieving page from github'
        return
# end getPage()


def main():
    username = sys.argv[1]
    homepage = getPage('/' + username)
    followers = getPage('/' + username + '/followers')
    following = getPage('/' + username + '/following')
    starred = getPage('/' + username + '/starred')
