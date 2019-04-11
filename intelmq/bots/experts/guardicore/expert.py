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
        if 'unavailable' in web_soup.find(attrs={"data-pintopage": "page_fixedCenter"}).text:
            self.send_message(event)
        else:
            host_type = web_soup.find('span', attrs={"class": "verdict-label"}).text
            if host_type == 'Malicious':
                table = web_soup.find_all("table")
                tags = []
                servers = []
                ports = []
                for row in table[0].find_all("tr"):
                    column = row.find_all('td')
                    data = [data.text.strip() for data in column]
                    if data[0] == 'Role':
                        tags.append(data[1])
                    if data[0] == 'Tags':
                        for tag in column[1].find_all("span"):
                            tags.append(tag.text)
                    if data[0] == 'Ports Scanned':
                        for port in column[1].find_all("span"):
                            ports.append(port.text)
                    if ip:
                        if data[0] == "Connect Back Servers":
                            for server in column[1].find_all(href=re.compile("domain")):
                                servers.append(server.text)
                if not ip:
                    ip_add = table[1].find("tr").find_all('td')[1].text.strip()
                    event.add("source.ip", ip_add, raise_failure=False)
                if tags:
                    event.add("extra.tags", tags)
                if ports:
                    event.add("extra.dest_port", ports)
                if servers:
                    for server in servers:
                        event.add("source.fqdn", server, overwrite=True)
                        self.send_message(event)
                else:
                    self.send_message(event)

        self.acknowledge_message()


BOT = GuardicoreExpertBot
