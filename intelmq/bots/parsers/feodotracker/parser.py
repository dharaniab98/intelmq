# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup as bs

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class FeodoTrackerParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        soup = bs(raw_report, 'html.parser')
        feed_list = soup.find_all('tr')[1:]

        for feed in feed_list:
            data = feed.find_all('td')

            event = self.new_event(report)
            event.add('source.ip', data[2].text)
            event.add('status', data[3].text)
            event.add('time.source', data[0].text + 'UTC')
            event.add('classification.type', 'c&c')
            if data[1].text == 'E':
                event.add('malware.name', 'Emotet')
            elif data[1].text == 'C':
                event.add('malware.name', 'Geodo')
            else:
                event.add('malware.name', 'Dridex')

            if data[7].text != 'never':
                event.add('extra.last_seen', data[7].text)
            if data[4].text != 'Not listed':
                event.add('extra.SBL', data[4].text)

            event.add('raw', feed)
            self.send_message(event)

        self.acknowledge_message()


BOT = FeodoTrackerParserBot
