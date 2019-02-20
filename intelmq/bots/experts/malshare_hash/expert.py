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
        tables = web_data.find_all('table')
        if tables:
            for table in tables:
                if 'Hashes' in table.find('th').text:
                    hashes = table.find_all('td')
                    event.add('malware.hash.sha1', hashes[1].text.split()[1], overwrite=True)
                    event.add('malware.hash.sha256', hashes[2].text.split()[1], overwrite=True)
                elif 'Details' in table.find('th').text:
                    file_type = (table.find('td').text.split('File Type:')[1]).strip()
                    if file_type != '-':
                        event.add('extra.file_type', file_type, overwrite=True)
                elif 'Yara Hits' in table.find('th').text:
                    yara_rules = ','.join([i.strip() for i in table.find('td').text.split('|')[:-1]])
                    if yara_rules != '':
                        event.add('extra.yara_rules', yara_rules)
                elif 'Source' in table.find('th').text:
                    for urls in table.find_all('td'):
                        event.add('source.url', urls.text, overwrite=True)
                        self.send_message(event)
            if event.get('source.url') is None:
                self.send_message(event)
        else:
            self.send_message(event)
        self.acknowledge_message()


BOT = MalshareHashExpertBot
