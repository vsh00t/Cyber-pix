import json,os,requests, datetime
import sqlite3
from datetime import datetime
from zipfile import ZipFile
import settings
home = settings.home
url = settings.url
source = requests.get(url)
data = source.json()
database = settings.database
con = sqlite3.connect(database)
cur = con.cursor()
i = 0

for item in data:
    if item['bounty'] == 1 or item['bounty'] == 0:
        nombre = item['name']
        cuenta = item['count']
        cur.execute("SELECT name FROM chaos WHERE name == ?", (nombre, ))
        data = cur.fetchall()
        print(item['name'])
        if len(data) != 0:
            print(len(data))
            cur.execute("SELECT name, count, URL FROM chaos WHERE name == ?", (nombre,))
            for name, count, URL in cur.fetchall():
                print(cuenta, count)
                if cuenta > count:

                    print("hay nuevos en" + nombre)
                    # Download
                    print(URL)
                    filename = URL.split("/")[3]
                    r = requests.get(URL, allow_redirects=True)
                    now = datetime.now()
                    open( home+'data/' + filename, 'wb').write(r.content)
                    scanned = 0
                    with ZipFile(home + 'data/' + filename, 'r') as zipObj:
                        listOfiles = zipObj.namelist()
                        for file in listOfiles:
                            try:
                                cur.execute("INSERT INTO targets VALUES (?, ?, ?, ?)", (name, file, scanned, '0'))
                                con.commit()
                            except:
                                cur.execute("UPDATE targets SET scanned = ? WHERE name = ?", (scanned, name))
                                con.commit()
                        zipObj.extractall(home + 'data/')
                    os.remove(home + 'data/' + filename)
                    cur.execute("UPDATE chaos SET downloaded = '1' WHERE URL = ? and name = ?", (URL, name))
                    cur.execute("UPDATE chaos SET downloaded_date = ? WHERE URL = ?", (now, URL))
                    cur.execute("UPDATE chaos SET count = ? WHERE URL = ?", (cuenta, URL))
                    #cur.execute("UPDATE targets SET scanned = ? WHERE name = ?", (scanned, name))
                    con.commit()
        else:
            print(nombre)
            name = str(item['name'])
            program_url = str(item['program_url'])
            URL = str(item['URL'])
            count = int(item['count'])
            change = bool(item['change'])
            is_new = bool(item['is_new'])
            platform = str(item['platform'])
            bounty = str(item['bounty'])
            last_updated = (item['last_updated'])
            try:
                cur.execute("INSERT INTO chaos  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(name, program_url, URL, count, change, is_new, platform, bounty, last_updated, '0', '0'))
                con.commit()
            except:
                None
            print(URL)
            filename = URL.split("/")[3]
            r = requests.get(URL, allow_redirects=True)
            now = datetime.now()
            open(home + 'data/' + filename, 'wb').write(r.content)
            with ZipFile(home + 'data/' + filename, 'r') as zipObj:
                listOfiles = zipObj.namelist()
                for file in listOfiles:
                    try:
                        cur.execute("INSERT INTO targets VALUES (?, ?)", (name, file))
                        con.commit()
                    except:
                        None
                zipObj.extractall(home + 'data/')
            os.remove(home + 'data/' + filename)
            cur.execute("UPDATE chaos SET downloaded = '1' WHERE URL = ? and name = ?", (URL, name))
            con.commit()
            cur.execute("UPDATE chaos SET downloaded_date = ? WHERE URL = ?", (now, URL))
            con.commit()
con.close()
