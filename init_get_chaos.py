import json,os,requests
from datetime import datetime
import sqlite3
from zipfile import ZipFile
import settings
home = settings.home
url = "https://chaos-data.projectdiscovery.io/index.json"
source = requests.get(url)
data = source.json()
database = settings.database
con = sqlite3.connect(database)
cur = con.cursor()
i = 0
for item in data:
    if item['bounty'] == 0 or item['bounty'] == 1:

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
            cur.execute("INSERT INTO chaos  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(name, program_url, URL, count, change, is_new, platform, bounty, last_updated, '0', '0' ))
            con.commit()
        except:
            None

#Download
cur.execute("SELECT name, program_url, URL, count, change, is_new, platform, bounty, last_updated, downloaded FROM chaos")
for name, program_url, URL, count, change, is_new, platform, bounty, last_updated, downloaded in cur.fetchall():
    print(URL)
    filename = URL.split("/")[3]
    r = requests.get(URL, allow_redirects=True)
    now = datetime.now()
    open(home + 'data/'+filename, 'wb').write(r.content)
    with ZipFile(home + 'data/'+filename, 'r') as zipObj:
        listOfiles = zipObj.namelist()
        for file in listOfiles:
            try:
                cur.execute("INSERT INTO targets VALUES (?, ?, ?, ?)", (name, file, '0', '0'))
                con.commit()
            except:
                None
        zipObj.extractall( home + 'data/')
    os.remove(home + 'data/'+filename)
    cur.execute("UPDATE chaos SET downloaded = '1' WHERE URL = ? and name = ?", (URL,name))
    con.commit()
    cur.execute("UPDATE chaos SET downloaded_date = ? WHERE URL = ?", (now,URL))
    con.commit()

con.close()
