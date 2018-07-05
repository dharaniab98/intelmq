# -*- coding: utf-8 -*-

from datetime import datetime
from bs4 import BeautifulSoup as bs

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class HoneypotParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        soup = bs(raw_report, 'html.parser')

        feed_list = soup.find_all('tr')[1:-1]

        for feed in feed_list:
            data = feed.find_all('td')

            event = self.new_event(report)

            event.add('source.ip', data[0].text.strip().split('\xa0')[0])
            event.add('time.source', (datetime.strptime(data[3].text.strip(), '%Y-%m-%d')).isoformat() + 'UTC')
            event.add('classification.type', 'blacklist')
            event.add('extra.last_seen', data[4].text.strip())
            event.add('raw', feed)
            self.send_message(event)

        self.acknowledge_message()


BOT = HoneypotParserBot
