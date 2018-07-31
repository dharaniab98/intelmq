# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from datetime import datetime

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class URLVirHTMLParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        soup = bs(raw_report, 'html.parser')
        feed_list = soup.find_all('tr')[1:]

        for feed in feed_list:
            data = feed.find_all('td')

            event = self.new_event(report)
            event.add('source.ip', data[2].text.strip())
            event.add('malware.hash.md5', data[3].text)
            event.add('time.source', datetime.strptime(data[0].text, '%Y-%m-%d').isoformat() + 'UTC')
            event.add('status', data[5].text)
            event.add('classification.type', 'malware')
            event.add('raw', feed)
            self.send_message(event)

        self.acknowledge_message()


BOT = URLVirHTMLParserBot
