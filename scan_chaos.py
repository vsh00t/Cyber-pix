import os
import sqlite3
import settings
database = settings.database
resultados = settings.resultados
templates = settings.templates
home = settings.home
con = sqlite3.connect(database)
cur = con.cursor()
cur.execute("SELECT file, scanned FROM targets WHERE scanned != '1' and disable != '1' ORDER BY name DESC LIMIT 1")
os.system('nuclei -update-templates')
for file, scanned in cur.fetchall():
	print(file)
	cur.execute("UPDATE targets SET scanned = '1' WHERE file = ?", (file, ))
	con.commit()
	try:
		os.system ('touch '+ resultados +'/'+ file)
		os.system ('cat ' +home+ 'data/'+ file +'| /usr/local/bin/httpx -threads 5000 --silent | /usr/local/bin/nuclei --silent -c 800 -rl 2000 -t '+templates+' -o '+ resultados + '/'+ file)
		print(file + ' procesado correctamente')
	except:
		print('FAIL')
	try:
		os.system('cat ' + resultados + '/'+ file + ' | sendmsg.py')
	except:
		print('FAIL')
