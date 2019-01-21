# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

from intelmq.lib.bot import Bot
from intelmq.lib import utils


class VXVaultExpertBot(Bot):

    def process(self):
        event = self.receive_message()
        url = event.get("extra.vxvault_link")
        web_text = requests.get(url).text
        web_data = bs(web_text, 'html.parser')
        data = [data.next_sibling.strip() for data in web_data.find_all('b')]
        if data[0] != "sample":
            event.add('extra.filename', data[0])
        event.add('malware.hash.sha1', data[3])
        event.add('malware.hash.sha256', data[4])
        event.add('time.source', (datetime.strptime(data[7], '%Y-%m-%d')).isoformat() + 'UTC')
        self.send_message(event)
        self.acknowledge_message()


BOT = VXVaultExpertBot
