import http.cookiejar
import urllib.request
import urllib.parse
import logging
import json
import time
import os
import re

from bs4 import BeautifulSoup

logger = logging.getLogger( __name__ )
logger.setLevel( logging.DEBUG )
logger.addHandler( logging.FileHandler('Curr.log'));

class Curriculum( object ):
    def __init__( self ):
        self.data = ""
        with open( 'postData.json', 'r', encoding='UTF-8' ) as file:
            data = json.load(file)

        self.WebTPcode1 = data['WebTPcode1']
        self.WebDiviCode1 = data['WebDiviCode1']
        self.WebDomainNo1 = data['WebDomainNo1']
        self.WebColCode1 = [
            "800:管理學院", \
            "700:人文藝術學院", \
            "600:師範學院", \
            "500:生命科學院", \
            "400:理工學院", \
            "300:農學院", \
            "000:虛擬學院" \
        ]

    def _Opener( self, head ):
        cookie = http.cookiejar.CookieJar()
        processor = urllib.request.HTTPCookieProcessor( cookie )
        opener = urllib.request.build_opener( processor )
        header = []
        for key, value in head.items():
            elem = ( key, value )
            header.append( elem )
        opener.addheaders = header
        return opener

    def run( self, year = 104, semester = 1 ):
        self.get_pub_clata3( year, semester)
        self.get_pub_clata4( year, semester)
        self.get_pub_clata5( year, semester)

    def get_pub_clata3( self, year, semester ):
        url = "https://web085003.adm.ncyu.edu.tw/pub_clata3.aspx"
        save_path = os.path.join( '.', 'data' )

        for code1 in self.WebDiviCode1:             # 學院
            for code2 in code1:                     # 學系
                for domain in self.WebDomainNo1:    # 課程類別
                    for grade in range( 1, 7+1 ):   # 年級
                        # time.sleep( 5 )
                        print( "{}, {}, {}".format( code2, domain, grade ) )
                        postDict = {
                            'WebPid1' : '',
                            'Language' : 'zh-TW',
                            'WebYear1' : str( year ).zfill(3),
                            'WebTerm1' : str( semester ),
                            'WebPDC99' : self.WebTPcode1[0].split(':')[1],
                            'WebDiviCode1': code2,
                            'WebDomainNo1': domain,
                            'WebCrsGrade1': str( grade )
                        }
                        for retry in range( 5 ):
                            try:
                                WebColCode1 = self.get_data( url, postDict )
                            except:
                                logger.warning( "retry {} at {}, {}, {}, {}, {}".format( retry, year, semester, code2, domain, grade ) )
                            else:
                                break

                        if WebColCode1 == None:
                            continue
                        # for data in WebColCode1:
                        #     print( data )

                        if not os.path.exists( "data" ):
                            os.mkdir( "data" )

                        p = re.compile( ':' )

                        with open( os.path.join( save_path, p.sub( '_',str(year) + '_' + str(semester) + '_' + str(code2) + "_" + domain + "_" + str(grade) ) ), 'w', encoding='UTF-8' ) as file:
                            file.write( json.dumps( WebColCode1, indent = 4, ensure_ascii=False ) )

        return

    def get_pub_clata4( self, year, semester ):
        pass

    def get_pub_clata5( self, year, semester ):
        pass

    def get_data( self, url, postDict ):
        header = {
        }

        opener = self._Opener( header )
        postData = urllib.parse.urlencode(postDict).encode()

        data = opener.open( url, postData, 5 ).read()

        soup = BeautifulSoup( data.decode( 'big5','ignore' ), "html5lib" )

        first = True
        for child in soup.body.children:
            if child.name == 'table' or child.name == u'table':
                if first:
                    first = False
                    continue
                tblh = child
                break

        trs = tblh.find_all('tr')
        if trs[1].find( 'td' ).get_text() == '\n查無任何開課資料!!\n':
            return

        data = []
        for index in range( 1, len(trs) ):
            tds = trs[index].find_all('td')
            part = [];
            for index2 in range( len(tds) ):
                part.append( tds[index2].get_text() )
            data.append( part )

        return data

if __name__ == '__main__':
    curr = Curriculum()
    for year in range( 99, 89, -1 ):
        for semester in [ 1, 2 ]:
            if year == 103 and semester == 2:
                continue
            curr.run( year, semester )
