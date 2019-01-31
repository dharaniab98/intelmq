# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class MalshareParserBot(Bot):

    def process(self):
        report = self.receive_message()
        text = utils.base64_decode(report['raw'])

        soup = bs(text, 'html.parser')
        feed_list = soup.find_all('tr')[1:]

        for feed in feed_list:
            data = feed.find_all('td')

            event = self.new_event(report)
            event.add('time.source', data[2].text)
            event.add('classification.type', 'malware')
            event.add('malware.hash.md5', data[0].text)
            event.add('extra.file_type', data[1].text)
            event.add('raw', feed)
            self.send_message(event)

        self.acknowledge_message()


BOT = MalshareParserBot
