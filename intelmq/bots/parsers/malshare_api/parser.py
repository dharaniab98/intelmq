# -*- coding: utf-8 -*-

import json

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class MalshareAPIParserBot(Bot):

    def process(self):
        report = self.receive_message()
        api_data = utils.base64_decode(report['raw'])

        feed_list = json.loads(api_data)

        for feed in feed_list:
            event = self.new_event(report)
            event.add('classification.type', 'malware')
            event.add('malware.hash.md5', feed['md5'])
            event.add('malware.hash.sha1', feed['sha1'])
            event.add('malware.hash.sha256', feed['sha256'])
            event.add('raw', json.dumps(feed))
            self.send_message(event)

        self.acknowledge_message()


BOT = MalshareAPIParserBot
