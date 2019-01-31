# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs

from intelmq.lib.bot import Bot
from intelmq.lib import utils


class MalshareHashExpertBot(Bot):

    def process(self):
        event = self.receive_message()
        md5_hash = event.get("malware.hash.md5")
        web_text = requests.get("https://malshare.com/sample.php?action=detail&hash=" + md5_hash).text
        web_data = bs(web_text, 'html.parser')
        data = web_data.find_all('table')
        hashes = data[0].find_all('td')
        event.add('malware.hash.sha1', hashes[1].text.split()[1])
        event.add('malware.hash.sha256', hashes[2].text.split()[1])
        yara_rules = ','.join([i.strip() for i in data[2].find('td').text.split('|')[:-1]])
        if yara_rules != '':
            event.add('extra.yara_rules', yara_rules)
        if len(data) > 4:
            event.add('source.url', data[3].find('td').text)
        self.send_message(event)
        self.acknowledge_message()


BOT = MalshareHashExpertBot
