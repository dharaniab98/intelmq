# -*- coding: utf-8 -*-

import yaml
from datetime import datetime as dt, timedelta

from intelmq.lib import utils
from intelmq.lib.bot import Bot

FEEDS = {'attackers': ['attackers_data', 'malware'], 'malicious_domains': ['mal_domains', 'malware'],
         'malicious_cc': ['mal_cc', 'c&c'], 'scanners': ['scanners_data', 'scanner']}


class GuardicoreParserBot(Bot):
    def init(self):
        self.field = self.parameters.field
        now = dt.now()
        first_day = now - timedelta(now.isoweekday())
        ref_day = dt.strptime('2018-04-08', '%Y-%m-%d')
        self.index = ((first_day - ref_day).days) // 7 + 1

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        data = raw_report.split(FEEDS[self.field][0] + ' =')[2]
        feeds_data = yaml.load(data)
        if self.index in feeds_data:
            feeds = feeds_data[self.index][0] if self.field in ['attackers', 'scanners'] else feeds_data[self.index]
            for feed in feeds:
                event = self.new_event(report)
                event.add('classification.type', FEEDS[self.field][1])
                if self.field == 'malicious_domains':
                    event.add('source.fqdn', feed)
                else:
                    event.add('source.ip', feed)
                event.add('raw', feed)
                self.send_message(event)
        self.acknowledge_message()


BOT = GuardicoreParserBot
