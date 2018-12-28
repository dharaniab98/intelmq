# -*- coding: utf-8 -*-

from datetime import datetime
from bs4 import BeautifulSoup as bs

from intelmq.lib import utils
from intelmq.lib.bot import Bot

host_type = {1: "Bulletproof", 2: "Compromised site", 3: "Free webhosting", 5: "Fastflux hosted"}


class ZeusTrackerParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        soup = bs(raw_report, 'html.parser')
        table_data = soup.find_all('table')[1]
        feed_list = table_data.find_all('tr')[1:]

        for feed in feed_list:
            data = feed.find_all('td')

            event = self.new_event(report)
            event.add('source.ip', data[3].text, raise_failure=False)
            event.add('source.fqdn', data[2].text, raise_failure=False)
            event.add('time.source', datetime.strptime(data[0].text.strip(), '%Y-%m-%d').isoformat() + "UTC")
            event.add('classification.type', 'c&c')
            event.add('malware.name', data[1].text)
            if data[4].text != '4':
                event.add('extra.host_type', host_type[int(data[4].text)])
            if data[5].text != 'unknown':
                event.add('extra.status', data[5].text)
            if data[7].text != 'Not listed':
                event.add('extra.sbl', data[7].text)
            event.add('raw', feed)
            self.send_message(event)

        self.acknowledge_message()


BOT = ZeusTrackerParserBot
