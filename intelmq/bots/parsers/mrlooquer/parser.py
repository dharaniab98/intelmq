# -*- coding: utf-8 -*-

import io
import csv
import json
from datetime import datetime

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot


class MrlooquerParserBot(ParserBot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        csv_reader = csv.reader(io.StringIO(raw_report), delimiter=',')
        next(csv_reader)
        for data in csv_reader:
            event = self.new_event(report)
            event.add('source.fqdn', data[0])
            event.add('source.ip', data[1])
            event.add('source.asn', data[2])
            event.add('extra.destination_port', (data[4])[1:-1].split(','))
            if data[10] == 'malware':
                event.add('classification.type', 'malware')
                if data[12] not in ["malware", "compromised", "elf", "C&C", "botnet", "trojan"]:
                    event.add('malware.name', data[12])
                event.add('extra.tags', [data[11], data[12]])
            elif data[10] == 'fraud':
                event.add('classification.type', 'phishing')
            elif data[10] == 'anonymization':
                event.add('classification.type', 'tor')
            event.add('raw', json.dumps(data))
            self.send_message(event)

        self.acknowledge_message()


BOT = MrlooquerParserBot
