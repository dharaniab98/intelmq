# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt

from intelmq.lib.bot import Bot
from intelmq.lib import utils


class FeodoTrackerExpertBot(Bot):

    def process(self):
        event = self.receive_message()
        ip = event.get("source.ip")
        web_text = requests.get("https://feodotracker.abuse.ch/browse/host/" + ip).text
        web_soup = bs(web_text, 'html.parser')
        feeds = web_soup.find_all('table')
        if len(feeds) > 1:
            for feed in feeds[1].find_all('tr')[1:]:
                data = feed.find_all('td')
                event.add('malware.hash.md5', data[1].text, overwrite=True)
                event.add('source.port', data[4].text, overwrite=True)
                event.add('time.source', (dt.strptime(data[0].text, '%Y-%m-%d %H:%M:%S')).isoformat() + 'UTC', overwrite=True)
                self.send_message(event)
        self.acknowledge_message()


BOT = FeodoTrackerExpertBot
