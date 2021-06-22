#!/usr/bin/env python3
import requests
import sys
import time
import settings
CHAT_ID=settings.CHAT_ID
bot = settings.bot

for line in sys.stdin:
        if __name__ == '__main__':
                requests.post('https://api.telegram.org/'+ bot + '/sendMessage',data={'chat_id': CHAT_ID, 'text': line})
                time.sleep(2)
