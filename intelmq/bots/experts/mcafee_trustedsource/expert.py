# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from intelmq.lib.bot import Bot
from intelmq.lib import utils


class McafeeTrustedSourceExpertBot(Bot):
    def process(self):
        event = self.receive_message()
        url = event.get('source.url')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5)',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept-Language': 'en-US,en;q=0.9,de;q=0.8'}

        base_url = 'http://www.trustedsource.org/sources/index.pl'
        r = requests.get(base_url, headers=headers)
        bs = BeautifulSoup(r.content, "html.parser")
        form = bs.find("form", {"class": "contactForm"})
        token1 = form.find("input", {'name': 'e'}).get('value')
        token2 = form.find("input", {'name': 'c'}).get('value')

        headers['Referer'] = base_url

        payload = {'e': (None, token1),
                   'c': (None, token2),
                   'action': (None, 'checksingle'),
                   'product': (None, '01-ts'),
                   'url': (None, url)}

        r = requests.post('https://www.trustedsource.org/en/feedback/url', headers=headers, files=payload)

        bs = BeautifulSoup(r.text, 'html.parser')
        table = bs.find("table", {"class": "result-table"})
        td = table.find_all('td')
        category = td[3].text[2:]
        risk = td[4].text
        event.add('extra.mcafee_categorization', category.replace('<br />-', ','))
        event.add('extra.mcafee_reputation', risk)
        self.send_message(event)
        self.acknowledge_message()


BOT = McafeeTrustedSourceExpertBot
