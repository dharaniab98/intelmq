# -*- coding: utf-8 -*-

from datetime import datetime

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class BenkowParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        feed_list = raw_report.split('\n')
        for feed in feed_list[1:-1]:
            columns = (feed.replace('";;"', '";"";"').split('";"'))[1:5]
            event = self.new_event(report)
            event.add('malware.name', columns[0])
            if(columns[1].startswith('http://')):
                event.add('source.url', columns[1])
            else:
                event.add('source.url', 'http://' + columns[1])
            event.add('source.ip', columns[2], raise_failure=False)
            event.add('classification.type', 'malware')
            event.add('time.source', (datetime.strptime(columns[3].replace('";', ''),\
                                         '%d-%m-%Y')).isoformat() + 'UTC')
            event.add('raw', feed)
            self.send_message(event)

        self.acknowledge_message()


BOT = BenkowParserBot
