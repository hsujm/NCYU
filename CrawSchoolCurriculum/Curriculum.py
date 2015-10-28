import http.cookiejar
import urllib.request
import urllib.parse
import sqlite3
import json

from bs4 import BeautifulSoup


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

    def run( self ):
        data = []
        data.append( self.get_pub_clata3() )
        data.append( self.get_pub_clata4() )
        data.append( self.get_pub_clata5() )
        with open( 'data.txt', 'w', encoding='UTF-8' ) as file:
            file.write( json.dumps( data, indent = 4 ) )
        
    def get_pub_clata3( self ):
        url = "https://web085003.adm.ncyu.edu.tw/pub_clata3.aspx"
        
        for code1 in self.WebDiviCode1:
            for code2 in code1:
                for domain in self.WebDomainNo1:
                    for grade in range( 1, 7+1 ):
                        print( "{}, {}, {}".format( code2, domain, grade ) )
                        postDict = {
                            'WebPid1' : '',
                            'Language' : 'zh-TW',
                            'WebYear1' : str(104),
                            'WebTerm1' : str(1),
                            'WebPDC99' : self.WebTPcode1[0].split(':')[1],
                            'WebDiviCode1': code2,
                            'WebDomainNo1': domain,
                            'WebCrsGrade1': str( grade )
                        }
                        WebColCode1 = self.get_data( url, postDict )
                        if WebColCode1 == None:
                            continue
                        for data in WebColCode1:
                            print( data )
        return
        
    def get_pub_clata4( self ):
        pass
    
    def get_pub_clata5( self ):
        pass
    
    def get_data( self, url, postDict ):
        header = {
        }
    
        opener = self._Opener( header )
        postData = urllib.parse.urlencode(postDict).encode()
        data = opener.open( url, postData ).read()
        
        soup = BeautifulSoup( data.decode( 'big5','replace' ), "html5lib" )
        
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
    curr.run()