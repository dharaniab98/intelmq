# -*- coding: utf-8 -*-
import json
from dateutil import parser

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class IscSansIpParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        lines = raw_report.split('\n')
        for line in lines:
            if not line: 
                continue
            if line.startswith('#'):
                continue
            event = self.new_event(report)

            data = line.split('\t')
            ip = '.'.join([str(int(i)) for i in data[0].split('.')])
            event.add('source.ip', ip)
            event.add('classification.type', 'blacklist')
            event.add('time.source', parser.parse(data[3]).isoformat() + 'UTC')
            event.add('extra.last_seen', data[4])
            event.add('raw', line)
            self.send_message(event)

        self.acknowledge_message()


BOT = IscSansIpParserBot
