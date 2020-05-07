# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from datetime import datetime

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot

SOURCE_FEEDS = {'https://precisionsec.com/threat-intelligence-feeds/agenttesla': 'agent-tesla',
                'https://precisionsec.com/threat-intelligence-feeds/emotet': 'emotet',
                'https://precisionsec.com/threat-intelligence-feeds/gandcrab': 'gandcrab',
                'https://precisionsec.com/threat-intelligence-feeds/njrat': 'njrat',
                'https://precisionsec.com/threat-intelligence-feeds/lokibot': 'lokibot',
                'https://precisionsec.com/threat-intelligence-feeds/trickbot': 'trickbot',
                'https://precisionsec.com/threat-intelligence-feeds/ursnif': 'ursnif'}


class PrecisionsecParserBot(ParserBot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        soup = bs(raw_report, 'html.parser')
        feed_list = soup.find_all('tr')[1:]

        for feed in feed_list:
            data = feed.find_all('td')

            if data[0].text == '':
                continue

            event = self.new_event(report)
            try:
                event.add('source.url', data[0].text)
            except:
                event.add('source.ip', data[0].text.split(':')[0])
                event.add('source.port', data[0].text.split(':')[1])
            event.add('time.source', datetime.strptime(data[1].text.strip(), '%Y-%m-%d %H:%M:%S').isoformat() + "UTC")
            event.add('classification.type', 'malware')
            event.add("malware.name", SOURCE_FEEDS[report["feed.url"]])
            event.add("raw", feed)
            self.send_message(event)

        self.acknowledge_message()


BOT = PrecisionsecParserBot
