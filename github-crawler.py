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
# end printFollowers()


def printFollowing(count):
    global following

    print (format + '|__ Following:')%' ', count
    temp = following.find(' Following')
    following = following[(temp + 1):]
    temp = following.find(' Following')
    following = following[(temp+1):]

    for i in range(count):
        temp = following.find('<li>')
        following = following[temp:]
        aTagStart = following.find('<a')
        aTagEnd = following.find('"><')
        em = following.find('<em>')
        emE = following.find('</em>')
        print format%' ', '  ', i + 1, '\b.', following[(aTagStart+10) : aTagEnd], following[(em+4) : (emE)]

        following = following[emE:]
# end printFollowing()


def printStarredRepos(count):
    global following

    print (format + '|__ Starred Repos:')%' ', count
    for i in range(count):
        temp = following.find('<li')
        following = following[temp:]
        aTagStart = following.find('<a')
        aTagEnd = following.find('" class')
        print (format+'|')%' ', '  ', i + 1, '\b.', following[(aTagStart+10) : aTagEnd]

        following = following[(aTagEnd+1):]
# end printStarredRepos()


def printRepos(username):
    # TODO
    # if repo is empty or forked
    global homepage

    print
    print username, '\b\'s Repositories'

    start = homepage.find('class="public')
    while not (start == -1):
        homepage = homepage[start:]

        temp1 = homepage.find('<li')
        temp2 = homepage.find('</li>')
        language = homepage[(temp1+4) : temp2]

        temp1 = homepage.find('<h3>')
        homepage = homepage[(temp1+1):]
        temp1 = homepage.find('<a')
        homepage = homepage[temp1:]
        temp1 = homepage.find('">')
        temp2 = homepage.find('</a>')
        name = homepage[(temp1 + 2) : temp2]

        temp1 = homepage.find('<p')
        temp2 = homepage.find('</p>')
        description = homepage[(temp1+23) : temp2]

        print 'Name:', name
        print 'Language:', language
        print 'Description:', description

        homepage = homepage[temp2:]
        start = homepage.find('class="public')
# end printRepos()


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

    print (format + '|')%' '
    printFollowers(followersCount)
    print (format + '|')%' '
    printFollowing(followingCount)
    print (format + '|')%' '
    printStarredRepos(starsCount)
# end main()


if __name__ == '__main__':
    main()
