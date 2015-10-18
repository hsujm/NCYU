
import http.cookiejar
import urllib.request
import urllib.parse
import sqlite3

from bs4 import BeautifulSoup

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

def main():
    # preset
    #http.client.HTTPConnection.debuglevel = 1 # debug
    url = "https://web085003.adm.ncyu.edu.tw/pub_wrec340b.aspx"
    postDict = {
        'WebPid1' : '',
        'Language' : 'zh-TW',
        'WebCampus' : '',
        'WebCollege' : '',
        'WebProgram' : ''
    }
    header = {
    }

    conn = sqlite3.connect( 'NoS.db' )
    cursor = conn.cursor()

    opener = Opener( header )
    postData = urllib.parse.urlencode(postDict).encode()
    data = opener.open( url, postData ).read()
    soup = BeautifulSoup( data.decode( 'big5'), "lxml" )

    cursor.execute( '''CREATE TABLE IF NOT EXISTS NoS (
    division varchar(20),
    college varchar(20),
    edusystem varchar(20),
    department varchar(60),
    first_grade_boy integer,
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
    primary key( division, college, edusystem, department ) )''' )

    tblh = soup.find_all( 'table' )
    print( len( tblh ) )
    tblh = tblh[2];
    trs = tblh.find_all('tr')
    sql = 'INSERT INTO NoS VALUES ({seq})'.format( seq = ','.join( ['?']*23 ) )

    for index in range( 2, len(trs)-1 ):
        tds = trs[index].find_all('td')
        part = [];
        for index2 in range( len(tds) ):
            part.append( tds[index2].get_text() )
        cursor.execute( sql, part )
    print( soup.title.text )
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
