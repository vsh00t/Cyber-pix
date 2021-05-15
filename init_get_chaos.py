import json,os,requests
from datetime import datetime
import sqlite3
from zipfile import ZipFile

url = "https://chaos-data.projectdiscovery.io/index.json"
source= requests.get(url)
data = source.json()
database = "/home/jorge/bdd_cyber-pix.db"
con = sqlite3.connect(database)
cur = con.cursor()
i = 0
for item in data:
    if item['bounty'] == 1:
        #print(item['name'],item['URL'],item['platform'])
        #cur.execute("SELECT * FROM chaos")

        name = str(item['name'])
        program_url = str(item['program_url'])
        URL = str(item['URL'])
        count = int(item['count'])
        change = bool(item['change'])
        is_new = bool(item['is_new'])
        platform = str(item['platform'])
        bounty = str(item['bounty'])
        last_updated = (item['last_updated'])
        cur.execute("INSERT INTO chaos  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(name, program_url, URL, count, change, is_new, platform, bounty, last_updated, '0', '0' ))
        con.commit()

#Download
cur.execute("SELECT name, program_url, URL, count, change, is_new, platform, bounty, last_updated, downloaded FROM chaos WHERE bounty = 'True'")
for name, program_url, URL, count, change, is_new, platform, bounty, last_updated, downloaded in cur.fetchall():
    print(URL)
    filename = URL.split("/")[3]
    r = requests.get(URL, allow_redirects=True)
    now = datetime.now()
    open('data/'+filename, 'wb').write(r.content)
    with ZipFile('data/'+filename, 'r') as zipObj:
        zipObj.extractall('data/')
    os.remove('data/'+filename)
    cur.execute("UPDATE chaos SET downloaded = '1' WHERE URL = ? and name = ?", (URL,name))
    cur.execute("UPDATE chaos SET downloaded_date = ? WHERE URL = ?", (now,URL))
    con.commit()

con.close()
        #"name": "pythonanywhere",
        #"program_url": "https://help.pythonanywhere.com/pages/BugBounty",
        #"URL": "https://chaos-data.projectdiscovery.io/pythonanywhere.zip",
        #"count": 19998,
        #"change": 0,
        #"is_new": false,
        #"platform": "",
        #"bounty": true,
        #"last_updated": "2021-05-06T00:22:30.400742316Z"
#print(data)