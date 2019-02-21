# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs

from intelmq.lib.bot import Bot
from intelmq.lib import utils


class NortonExpertBot(Bot):

    def process(self):
        event = self.receive_message()
        host = event.get("source.fqdn")
        if host is None:
            host = event.get("source.ip")
        web_text = requests.get("https://safeweb.norton.com/report/show_mobile?name=" + str(host)).text
        web_soup = bs(web_text, 'html.parser')
        ref_div = web_soup.find('div', id='detail-1')
        if ref_div is None:
            self.send_message(event)
        names = ref_div.find_all_next(class_='span3')
        values = ref_div.find_all_next(class_='span9')
        for index in range(len(values)):
            name = names[index].text.strip()
            value = values[index].text.replace('Direct Link To', '').strip()
            if 'Threat Name' in name:
                event.add('extra.threat_info', value, overwrite=True)
            if 'Location' in name:
                event.add('source.url', value, overwrite=True)
                self.send_message(event)
        self.acknowledge_message()


BOT = NortonExpertBot
