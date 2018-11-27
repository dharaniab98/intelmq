# -*- coding: utf-8 -*-

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot


class TorQueryParserBot(ParserBot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        feed_list = raw_report.split('\n')
        flags = {8: 'Authority', 9: 'Exit', 10: 'Fast', 11: 'Guard', 12: 'Named', 13: 'Stable',
                 14: 'Running', 15: 'Valid', 16: 'V2Dir', 18: 'Hibernating', 19: 'Bad Exit'}

        for feed in feed_list[1:]:
            if feed is '':
                continue

            tor_flags = []
            data = feed.split(',')
            tor_flags = [flags[flag] for flag in flags if data[flag] is '1']

            event = self.new_event(report)
            event.add('source.ip', data[4])
            event.add('extra.tor_flags', tor_flags)
            event.add('classification.type', 'tor')
            event.add("raw", feed)
            self.send_message(event)

        self.acknowledge_message()


BOT = TorQueryParserBot
