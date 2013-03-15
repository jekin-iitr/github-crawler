#!/usr/bin/env python

# Prakash Gamit <prakashgamit23@gmail.com>
# Indian Institute of Technology, Roorkee

from httplib import *
import sys

# global connection object
conn=''

# variables holding different pages as strings
homepage = ''
followers = ''
following = ''
starred = ''
format = ''


# fetch page from github
def getPage(url):
    global conn
    conn.request('GET', url)

    response = conn.getresponse()

    if response.status == 200:
        return response.read()
    else:
        print 'Error retrieving page %s'%url, 'from github'
        return
# end getPage()


def parseHomePage():
    start = homepage.find('itemprop="name"')
    end = homepage[start:].find('<')
    print (format + '|__ Name:')%' ', homepage[(start+16) : (start+end)]

    start = homepage.find('itemprop="worksFor"')
    end = homepage[start:].find('<')
    print (format + '|__ Works for:')%' ', homepage[(start+20) : (start+end)]

    start = homepage.find('itemprop="homeLocation"')
    end = homepage[start:].find('<')
    print (format + '|__ Home Location:')%' ', homepage[(start+24) : (start+end)]

    start = homepage.find('join-date')
    end = homepage[start:].find('<')
    print (format + '|__ Joined on:')%' ', homepage[(start+11) : (start+end)]
# end parseHomePage()


# return followers, following and stars count
# @what => followers | following | stars
def getCount(what):
    temp = homepage.find(what)
    f1 = homepage[temp:]
    start = f1.find('<')
    end = f1.find('</')
    return int(f1[(start+8) : end])
# end getCount()


def printFollowers(count):
    global followers

    print (format + '|__ Followers:')%' ', count
    temp = followers.find('Followers')
    followers = followers[(temp + 1):]
    temp = followers.find('Followers')
    followers = followers[(temp+1):]

    for i in range(count):
        temp = followers.find('<li>')
        followers = followers[temp:]
        aTagStart = followers.find('<a')
        aTagEnd = followers.find('"><')
        em = followers.find('<em>')
        emE = followers.find('</em>')
        print format%' ', '  ', i + 1, '\b.', followers[(aTagStart+10) : aTagEnd], followers[(em+4) : (emE)]

        followers = followers[emE:]
# end getFollowers()


def main():
    global conn
    conn = HTTPSConnection('github.com')

    global homepage, followers, following, starred

    username = sys.argv[1]
    homepage = getPage('/' + username)
    followers = getPage('/' + username + '/followers')
    following = getPage('/' + username + '/following')
    starred = getPage('/' + username + '/starred')

    conn.close()

    format = '%' + str(len(username)/2) + 's'

    # parse homepage
    print username
    parseHomePage()

    followersCount = getCount('followers')
    followingCount = getCount('following')
    starsCount = getCount('stars')

    printFollowers(followersCount)
# end main()


if __name__ == '__main__':
    main()
