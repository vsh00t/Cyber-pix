import json
import requests
import sqlite3
import validators
from datetime import datetime
from datetime import timedelta
import settings


URL = "https://api.telegram.org/bot{}/".format(settings.token)
database = settings.database

con = sqlite3.connect(database)
cur = con.cursor()

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    if num_updates > 1:
        for i in range(1,int(num_updates)):
            try:
                text = updates["result"][i]["message"]["text"]
                chat_id = updates["result"][i]["message"]["chat"]["id"]
                update_id = updates["result"][i]["update_id"]
                t = cur.execute("SELECT domain,file, id, activo FROM external WHERE id = ?", (update_id,))
                result = cur.fetchone()
                if result:
                    print("El valor ya existe")
                else:
                    cur.execute("SELECT domain,file, id, activo FROM external")
                    result1 = cur.fetchone()
                    # print(result1)
                    if result1:
                        try:
                            v = validators.domain(text)
                            if v:
                                cur.execute("INSERT INTO external  VALUES (?, ?, ?, ?)", (text, text + ".txt", update_id, '1'))
                                con.commit()
                            else:
                                print("dominio no valido")
                        except:
                            print("dominio incorrecto.")
                    else:
                        print("usuario no autorizado")
            except:
                None
            #print(chat_id)
            #print(update_id)
            now = datetime.now()
            top = now + timedelta(hours=4)
            #a=1


        return (text, chat_id)
    else:
        print("No existen nuevos mensajes")


cur.execute("SELECT domain,file, id, activo FROM external ORDER BY id DESC LIMIT 1")
for domain,file, id, activo in cur.fetchall():
    last_update=id

text, chat = get_last_chat_id_and_text(get_updates())

con.close()
