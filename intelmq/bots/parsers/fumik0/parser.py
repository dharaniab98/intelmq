# -*- coding: utf-8 -*-

import json
from datetime import datetime

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class Fumik0ParserBot(Bot):

    def process(self):
        report = self.receive_message()
        api_data = utils.base64_decode(report['raw'])

        feed_list = json.loads(api_data)

        for feed in feed_list:
            event = self.new_event(report)
            event.add('classification.type', 'malware')
            event.add('malware.hash.md5', feed['hash']['md5'])
            event.add('malware.hash.sha1', feed['hash']['sha1'])
            event.add('malware.hash.sha256', feed['hash']['sha256'])
            event.add('time.source', datetime.strptime(feed['first_seen'], '%Y-%m-%d %H:%M:%S').isoformat() + "UTC")
            event.add('extra.file_name', feed['sample']['name'])
            event.add('extra.file_size', feed['sample']['size'])
            event.add('source.asn', feed['server']['AS'])
            event.add('source.ip', feed['server']['ip'])
            event.add('source.url', 'http://'+feed['server']['url'])
            event.add('source.fqdn', feed['server']['domain'])
            event.add('raw', json.dumps(feed))
            self.send_message(event)

        self.acknowledge_message()


BOT = Fumik0ParserBot
