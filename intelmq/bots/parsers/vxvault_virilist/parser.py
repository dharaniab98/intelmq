# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from datetime import datetime
import requests

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class VXVaultViriListParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        soup = bs(raw_report, 'html.parser')
        feed_list = soup.find_all('tr')[1:]

        feeds = [(i.find_all('a')[0]).get('href') for i in feed_list]

        for feed in feeds:

            url = 'http://vxvault.net/' + feed
            web_text = requests.get(url).text
            web_data = (bs(web_text, 'html.parser')).find(id='page')
            data = [data.next_sibling.strip() for data in web_data.find_all('b')]

            event = self.new_event(report)
            if data[0] != "sample":
                event.add('extra.filename', data[0])
            event.add('malware.hash.md5', data[2])
            event.add('malware.hash.sha1', data[3])
            event.add('malware.hash.sha256', data[4])
            event.add('source.url', data[5])
            event.add('source.ip', data[6])
            event.add('time.source', (datetime.strptime(data[7], '%Y-%m-%d')).isoformat() + 'UTC')
            event.add('extra.vxvault_link', url)
            event.add('classification.type', 'malware')
            event.add('raw', web_data)
            self.send_message(event)

        self.acknowledge_message()


BOT = VXVaultViriListParserBot
