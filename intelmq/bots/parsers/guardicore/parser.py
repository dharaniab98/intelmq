# -*- coding: utf-8 -*-

import yaml
from datetime import datetime as dt, timedelta

from intelmq.lib import utils
from intelmq.lib.bot import Bot

FEEDS = {'https://threatintelligence.guardicore.com/code/data/top_attackers.js': ['attackers_data', 'malware'],
         'https://threatintelligence.guardicore.com/code/data/malicious_domains.js': ['mal_domains', 'malware'],
         'https://threatintelligence.guardicore.com/code/data/malicious_cc.js': ['mal_cc', 'c&c'],
         'https://threatintelligence.guardicore.com/code/data/top_scanners.js': ['scanners_data', 'scanner']}


class GuardicoreParserBot(Bot):
    def init(self):
        now = dt.now()
        first_day = now - timedelta(now.isoweekday())
        ref_day = dt.strptime('2018-04-08', '%Y-%m-%d')
        self.index = str((first_day - ref_day).days // 7)

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        field, feed_type = FEEDS[report["feed.url"]]

        data = raw_report.split(field + ' =')[-1]
        feeds_data = yaml.load(data)
        if self.index in feeds_data:
            feeds = feeds_data[self.index][0] if field in ['attackers_data', 'scanners_data'] else feeds_data[self.index]
            for feed in feeds:
                event = self.new_event(report)
                event.add('classification.type', feed_type)
                if field == 'mal_domains':
                    event.add('source.fqdn', feed)
                else:
                    event.add('source.ip', feed)
                event.add('raw', feed)
                self.send_message(event)
        self.acknowledge_message()


BOT = GuardicoreParserBot
