# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class MaxmindParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        soup = bs(raw_report, 'html.parser')
        feed_list = soup.find_all('a','span3')

        for feed in feed_list:
            event = self.new_event(report)

            event.add('classification.type', 'vulnerable service')
            event.add('source.ip', feed.text.strip())
            event.add('raw', feed)
            self.send_message(event)
           
        self.acknowledge_message()


BOT = MaxmindParserBot
