import os
import sqlite3
import settings

database = settings.database
data = settings.data
templates = settings.templates
home = settings.home
ONEFORALL="/opt/OneForAll/oneforall.py "
con = sqlite3.connect(database)
cur = con.cursor()
cur.execute("SELECT domain,file, id, activo FROM external WHERE activo = '1' ORDER BY id ASC LIMIT 1")

for domain,file, id, activo in cur.fetchall():
    print(domain)
    os.system('python3 ' + ONEFORALL + ' --target ' + domain +' run')
    os.system('cat /opt/OneForAll/results/temp/collected_subdomains_' + domain + '* | sort | uniq > ' + data + domain + '.txt')

    try:
        cur.execute("INSERT INTO targets VALUES (?, ?, ?, ?)", (domain, file, '0', '0'))
        cur.execute("UPDATE targets SET scanned = '0' WHERE name = ? and file = ?", (domain, file))
        con.commit()
    except:
        cur.execute("UPDATE targets SET scanned = '0' WHERE name = ? and file = ?", (domain, file))
        con.commit()
    cur.execute("UPDATE external SET activo = '0' WHERE domain = ? and file = ?", (domain, file))
    con.commit()
