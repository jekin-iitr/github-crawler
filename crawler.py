
from httplib import *


class Crawler():
    def __init__(self, username):
        self.username = username

    def getpage(self):
        conn = HTTPSConnection('github.com')
        conn.request('GET', ('/' + self.username))
        response = conn.getresponse()

        if response.status == 200:
            homepage = response.read()
        else:
            print "Error getting the page from github"
            exit(1)

        conn.close()
        return homepage

