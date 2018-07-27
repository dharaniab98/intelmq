# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from datetime import datetime

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class BenkowRATParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        soup = bs(raw_report, 'html.parser')
        feed_list = soup.find_all('tr')[1:]

        for feed in feed_list:
            data = feed.find_all('td')

            event = self.new_event(report)
            event.add('source.url', 'http://' + data[3].text)
            event.add('source.ip', data[4].text, raise_failure=False)
            event.add('malware.name', data[2].text)
            event.add('time.source', datetime.strptime(data[1].text, '%d-%m-%Y').isoformat() + 'UTC')
            event.add('classification.type', 'malware')
            event.add('raw', feed)
            self.send_message(event)

        self.acknowledge_message()


BOT = BenkowRATParserBot
