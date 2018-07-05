# -*- coding: utf-8 -*-
import json

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class SigmaProjectsParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        feed_list = raw_report.split('\n')
        for feed in feed_list:
            if '/' not in feed:
                continue
            event = self.new_event(report)

            event.add('source.network', feed)
            event.add('classification.type', 'blacklist')
            event.add('raw', feed)
            self.send_message(event)

        self.acknowledge_message()


BOT = SigmaProjectsParserBot
