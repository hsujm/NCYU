import http.cookiejar
import urllib.request
import urllib.parse
import sqlite3
import json

from bs4 import BeautifulSoup


class Curriculum( object ):
    def __init__:
        self.data = ""
        with open( 'postData.json', 'r', encoding='UTF-8' ) as file:
            data = file.read()

        self.WebTPcode1 = data[ WebTPcode1 ]

    def _Opener( head ):
        cookie = http.cookiejar.CookieJar()
        processor = urllib.request.HTTPCookieProcessor( cookie )
        opener = urllib.request.build_opener( processor )
        header = []
        for key, value in head.items():
            elem = ( key, value )
            header.append( elem )
        opener.addheaders = header
        return opener
