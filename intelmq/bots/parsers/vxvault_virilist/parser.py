# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from datetime import datetime

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class VXVaultViriListParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        soup = bs(raw_report, 'html.parser')
        feed_list = soup.find_all('tr')[1:]
        current_year = datetime.now().year

        for feed in feed_list:
            data = feed.find_all('td')

            event = self.new_event(report)
            event.add('source.url', 'http://' + data[1].text.split('[D] ')[1])
            event.add('source.ip', data[3].text.strip())
            event.add('malware.hash.md5', data[2].text)
            feed_time = datetime.strptime(data[0].text, '%m-%d').replace(year=current_year)
            if feed_time < datetime.now():
                event.add('time.source', feed_time.isoformat() + 'UTC')
            else:
                event.add('time.source', (feed_time.replace(year=current_year - 1)).isoformat() + 'UTC')
            event.add('classification.type', 'malware')
            event.add('raw', feed)
            self.send_message(event)

        self.acknowledge_message()


BOT = VXVaultViriListParserBot
