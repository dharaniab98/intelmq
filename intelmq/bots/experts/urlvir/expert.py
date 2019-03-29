# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt

from intelmq.lib.bot import Bot
from intelmq.lib import utils


class URLvirExpertBot(Bot):

    def process(self):
        event = self.receive_message()
        url = event.get("event_description.url")
        if "search-ip-address" in url:
            url = url.replace("search-ip-address", "search-host")
        web_text = requests.get(url).text
        if web_text[223:237] == 'Host not found':
            url = url.replace("search-host/", "search-host/www.")
        web_text = requests.get(url).text
        web_soup = bs(web_text, 'html.parser')
        feeds = web_soup.find_all('table')
        if len(feeds) > 1:
            for feed in feeds[1:]:
                data = feed.find_all('td')
                event.add('malware.hash.md5', data[3].text, overwrite=True)
                event.add('source.ip', data[2].text, overwrite=True)
                event.add('time.source', dt.strptime(data[0].text, '%d-%m-%Y').isoformat()+' UTC', overwrite=True)
                event.add('source.url', data[1].text, overwrite=True)
                event.add('status', feeds[0].find_all('td')[-1].text, overwrite=True)
                self.send_message(event)
        else:
            event.add('time.source', dt.strptime(feeds[0].find('td').text, '%d-%m-%Y').isoformat()+ ' UTC', overwrite=True)
            event.add('status', feeds[0].find_all('td')[-1].text, overwrite=True)
            self.send_message(event)
        self.acknowledge_message()


BOT = URLvirExpertBot
