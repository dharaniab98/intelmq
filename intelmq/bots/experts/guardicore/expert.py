# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup as bs

from intelmq.lib.bot import Bot


class GuardicoreExpertBot(Bot):

    def process(self):
        event = self.receive_message()
        url = "http://threatintelligence.guardicore.com"
        ip = event.get("source.ip")
        if not ip:
            host = event.get("source.fqdn")
            web_text = requests.get(url + "/domain/" + host).text
        else:
            web_text = requests.get(url + "/ip/" + ip).text
        web_soup = bs(web_text, "html.parser")
        table = web_soup.find("table")
        tags = []
        servers = []
        for row in table.find_all("tr"):
            if "Tags" in row.text:
                for tag in row.find_all("span"):
                    tags.append(tag.text)
            if ip:
                if "Connect Back Servers" in row.text:
                    for server in row.find_all(href=re.compile("domain")):
                        servers.append(server.text)
        if tags:
            event.add("extra.tags", tags)
        if servers:
            for server in servers:
                event.add("source.fqdn", server, overwrite=True)
                self.send_message(event)
        else:
            self.send_message(event)
        self.acknowledge_message()


BOT = GuardicoreExpertBot
