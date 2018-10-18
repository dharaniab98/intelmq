# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from datetime import datetime

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot


class CybercrimeParserBot(ParserBot):
    def init(self):
        self.tags = []
        self.raw = ''
        self.info = []

    def parse(self, soup):
        for td in soup.findAll('td', attrs={'style': 'background-color: rgb(11, 11, 11);'}):
            if td.text != " ":
                self.info.append(td.text)
                self.raw += '%s' % (td)
                if len(self.info) % 4 == 0:
                    self.tags.append(self.info)
                    self.tags[len(self.tags) - 1].append(self.raw)
                    self.raw = ''
                    self.info = []

        return self.tags

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        soup = bs(raw_report, 'html.parser')
        data = self.parse(soup)
        for item in data:
            event = self.new_event(report)
            event.add('malware.name', 'atmos')
            try:
                event.add('time.source', datetime.strptime(item[1], '%d/%m/%Y %H:%M:%S').isoformat() + "UTC")
            except ValueError:
                continue
            event.add('source.fqdn', item[2], raise_failure=False)
            event.add('source.ip', item[2], raise_failure=False)
            event.add('malware.hash.md5', item[3])
            event.add('classification.type', 'c&c')
            event.add('raw', item[4])
            self.send_message(event)
        self.acknowledge_message()


BOT = CybercrimeParserBot
