# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class VXVaultViriListParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])

        soup = bs(raw_report, 'html.parser')
        feed_list = soup.find_all('tr')[1:]

        for feed in feed_list:
            data = feed.find_all('td')

            event = self.new_event(report)
            event.add('source.url', 'http://' + data[1].text.split('[D] ')[1])
            event.add('source.ip', data[3].text.strip())
            event.add('malware.hash.md5', data[2].text)
            event.add('extra.vxvault_link', 'http://vxvault.net/' + data[0].find('a').get('href'))
            event.add('classification.type', 'malware')
            event.add('raw', feed)
            self.send_message(event)

        self.acknowledge_message()


BOT = VXVaultViriListParserBot
