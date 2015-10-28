
import http.cookiejar
import urllib.request
import urllib.parse
import sqlite3
import json

from bs4 import BeautifulSoup

count = 0

def Opener( head ):
    cookie = http.cookiejar.CookieJar()
    processor = urllib.request.HTTPCookieProcessor( cookie )
    opener = urllib.request.build_opener( processor )
    header = []
    for key, value in head.items():
        elem = ( key, value )
        header.append( elem )
    opener.addheaders = header
    return opener

def get_code( year, semester, WebPDC99, WebColCode1, WebDomainNo1, Grade1 ):
    #preset
    global count 
    count += 1
    url = "https://web085003.adm.ncyu.edu.tw/pub_clata3.aspx"
    postDict = {
        'WebPid1' : '',
        'Language' : 'zh-TW',
        'WebYear1' : str(year),
        'WebTerm1' : str(semester),
        'WebPDC99' : WebPDC99,
        'WebDiviCode1': WebColCode1,
        'WebDomainNo1': WebDomainNo1,
        'WebCrsGrade1': str(Grade1)
    }
    header = {
    }

    opener = Opener( header )
    postData = urllib.parse.urlencode(postDict).encode()
    data = opener.open( url, postData ).read()
    # print( data.decode('big5','replace') )
    
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
    #sql = 'INSERT INTO NoS VALUES ({seq})'.format( seq = ','.join( ['?']*23 ) )
    data = []
    for index in range( 1, len(trs) ):
        tds = trs[index].find_all('td')
        part = [];
        for index2 in range( len(tds) ):
            part.append( tds[index2].get_text() )
        data.append( part )
        # cursor.execute( sql, part )
        # print( part )
        # conn.commit()
    
    return data

def main():
    # preset
    # http.client.HTTPConnection.debuglevel = 1 # debug
    with open( 'postData.json', 'r', encoding='UTF-8' ) as file:
        data = json.load(file)

    WebTPcode1 = data['WebTPcode1']
    WebDiviCode1 = data['WebDiviCode1']
    WebDomainNo1 = data['WebDomainNo1']
    WebColCode1 = [
        "800:管理學院", \
        "700:人文藝術學院", \
        "600:師範學院", \
        "500:生命科學院", \
        "400:理工學院", \
        "300:農學院", \
        "000:虛擬學院" \
    ]
    for code1 in WebDiviCode1:
        for code2 in code1:
            for domain in WebDomainNo1:
                for grade in range( 1, 7+1 ):
                    print( "{}, {}, {}".format( code2, domain, grade ) )
                    WebColCode1 = get_code( 104, 1, WebTPcode1[0].split(':')[1], code2, domain, grade )
                    if WebColCode1 == None:
                        continue
                    for data in WebColCode1:
                        print( data )
    return
    url = "https://web085003.adm.ncyu.edu.tw/pub_depta2.aspx"
    conn = sqlite3.connect( 'NCYUCurriculum.db' )
    cursor = conn.cursor()


    for year in range( 104, 104+1 ):
        for semester in range( 1, 7+1 ):
            cursor.execute( '''CREATE TABLE IF NOT EXISTS {} (
            curriculum_Category varchar(20),
            dep_num char(3),
            curriculum_name char(40),
            curriculum_num integer,
             integer,
            first_grade_girl integer,
            second_grade_boy integer,
            second_grade_girl integer,
            thrid_grade_boy integer,
            thrid_grade_girl integer,
            forth_grade_boy integer,
            forth_grade_girl integer,
            fifth_grade_boy integer,
            fifth_grade_girl integer,
            sixth_grade_boy integer,
            sixth_grade_girl integer,
            seventh_grade_boy integer,
            seventh_grade_girl integer,
            super_senior_boy integer,
            super_senior_girl integer,
            sum_boy integer,
            sum_girl integer,
            sum integer,
            primary key( division, college, edusystem, department ) )'''.format( "y{}_{}".format( year, semester ) ) )

            for department in dep_num:
                postDict = {
                    'WebPid1' : '',
                    'Language' : 'zh-TW',
                    'WebYear1' : str(year),
                    'WebTerm1' : str(semester),
                    'WebDep67' : str(department)
                }
                header = {
                }
                print( postDict )
                opener = Opener( header )
                postData = urllib.parse.urlencode(postDict).encode()
                data = opener.open( url, postData ).read()
                soup = BeautifulSoup( data.decode( 'big5'), "lxml" )

                tblh = soup.find_all( 'table' )
                tblh = tblh[3];
                trs = tblh.find_all('tr')
                if trs[1].find( 'td' ).get_text() == '\n查無任何開課資料!!\n':
                    continue
                #sql = 'INSERT INTO NoS VALUES ({seq})'.format( seq = ','.join( ['?']*23 ) )

                for index in range( 1, len(trs) ):
                    tds = trs[index].find_all('td')
                    part = [];
                    for index2 in range( len(tds) ):
                        part.append( tds[index2].get_text() )
                    # cursor.execute( sql, part )
                    print( part )
                    # conn.commit()
    # conn.close()
if __name__ == '__main__':
    main()
