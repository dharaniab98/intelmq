# -*- coding: utf-8 -*-

import json
from datetime import datetime

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class AZORultTrackerParserBot(Bot):

    def process(self):
        report = self.receive_message()
        api_data = utils.base64_decode(report['raw'])

        feed_list = json.loads(api_data)

        for feed in feed_list:
            event = self.new_event(report)
            event.add('classification.type', 'c&c')
            event.add('status', feed['status'])
            event.add('time.source', datetime.utcfromtimestamp(feed['first_seen']).isoformat() + " UTC")
            event.add('source.asn', feed['asn'])
            event.add('source.ip', feed['ip'])
            event.add('source.url', feed['panel_index'])
            event.add('source.fqdn', feed.get('domain'))
            event.add('raw', json.dumps(feed))
            self.send_message(event)

        self.acknowledge_message()


BOT = AZORultTrackerParserBot
