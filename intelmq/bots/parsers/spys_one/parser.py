# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from dateutil import parser

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class SpysOneParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        soup = bs(raw_report, 'html.parser')
        feed_list = soup.find_all('tr')[-28:-2]

        for feed in feed_list:
            data = feed.find_all('td')

            event = self.new_event(report)
            event.add('classification.type', 'proxy')
            event.add('source.ip', data[0].text.strip().split('\xa0')[0].split('document')[0])
            event.add('time.source', parser.parse(data[5].text.strip()).isoformat() + "UTC")
            event.add('raw', feed)
            self.send_message(event)
           
        self.acknowledge_message()


BOT = SpysOneParserBot
