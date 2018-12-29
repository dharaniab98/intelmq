# -*- coding: utf-8 -*-
from datetime import datetime
from bs4 import BeautifulSoup as bs

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot


class Aa419ParserBot(ParserBot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        soup = bs(raw_report, 'html.parser')

        feed_list = soup.find_all('tr')[1:-1]
        for feed in feed_list:
            item = feed.find_all('td')

            event = self.new_event(report)
            event.add('source.url', item[1].text.strip())
            event.add('extra.phishing_site', item[2].text.strip())
            event.add('extra.phishing_status', item[3].text.strip())
            event.add('extra.last_updated', item[5].text.strip())
            event.add('time.source', datetime.strptime(item[4].text.strip(), '%Y-%m-%d %H:%M').isoformat() + "UTC")
            event.add('classification.type', 'phishing')
            event.add('raw', feed)
            self.send_message(event)
        self.acknowledge_message()


BOT = Aa419ParserBot
