# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt

from intelmq.lib.bot import Bot
from intelmq.lib import utils


class AbusechZeuSExpertBot(Bot):

    def process(self):
        event = self.receive_message()
        host = event.get("source.fqdn")
        if not host:
            host = event.get("source.ip")
        web_text = requests.get('https://zeustracker.abuse.ch/monitor.php?host=' + host).text
        web_soup = bs(web_text, 'html.parser')
        if 'not found' in web_soup.find(attrs={"class": "ContentBox"}).find('p').text:
            self.send_message(event)
        else:
            tables = web_soup.find_all('table')
            rows = sum((_.find_all('tr')[1:] for _ in tables[1:4]), [])
            for row in rows:
                new_event = event.copy()
                data = row.find_all('td')
                if len(data) == 9:
                    try:
                        new_event.add('malware.hash.md5', data[6].text)
                    except:
                        new_event.add('malware.hash.md5', data[4].text)
                new_event.add('time.source', dt.strptime(data[0].text, '%Y-%m-%d').isoformat() + 'UTC', overwrite=True)
                new_event.add('source.url', "http://" + data[1].text)
                new_event.add('extra.status', data[2].text, overwrite=True)
                self.send_message(new_event)

        self.acknowledge_message()


BOT = AbusechZeuSExpertBot
