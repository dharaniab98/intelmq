# -*- coding: utf-8 -*-
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot


class AbusechThreatfoxParseBot(ParserBot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        soup = bs(raw_report, 'html.parser')

        feed_list = soup.find_all('tr')[1:-1]
        for feed in feed_list:
            item = feed.find_all('td')
            event = self.new_event(report)
            ioc_str = item[1].text.strip()
            if (ioc_str.startswith("http") != True) and ioc_str.find(":"):
                ioc_str = ioc_str.split(":")[0]
            if self.check_sha256(ioc_str):
                event.add('malware.hash.sha256', ioc_str)
            elif self.check_sha1(ioc_str):
                event.add('malware.hash.sha1', ioc_str)
            elif self.check_md5(ioc_str):
                event.add('malware.hash.md5', ioc_str)
            elif self.check_ip(ioc_str):
                event.add('source.ip', ioc_str)
            elif ioc_str.startswith('http'):
                event.add('source.url', ioc_str)
            event.add('malware.name', item[2].text.strip())
            event.add('extra.tags', item[3].text.strip().split(" "))
            event.add('time.source', datetime.strptime(item[0].text.strip(), '%Y-%m-%d %H:%M').isoformat() + "UTC")
            event.add('classification.type', 'malware')
            event.add('raw', feed)
            self.logger.info("started adding extra data")
            ioc_id = item[1].find('a')['href']
            http_url = f"https://threatfox.abuse.ch{ioc_id}"
            timeoutretries = 0
            #http_timeout_max_tries = 3
            resp = None

            while timeoutretries < 3 and resp is None:
                try:
                    resp = requests.get(url=http_url) #auth=self.auth,
                                        # proxies=self.proxy, headers=self.http_header,
                                        # verify=self.http_verify_cert,
                                        # cert=self.ssl_client_cert,
                                        # timeout=self.http_timeout_sec)

                except requests.exceptions.Timeout:
                    timeoutretries += 1
                    self.logger.warn("Timeout whilst downloading the report.")

            if resp is None and timeoutretries >= 3:
                self.logger.error("Request timed out %i times in a row.",
                                timeoutretries)
                continue

            if resp.status_code // 100 != 2:
                raise ValueError('HTTP response status code was %i.' % resp.status_code)
            else:
                soup_inner = bs(resp.text, 'html.parser')
                th_list = soup_inner.find_all('th')
                td_list = soup_inner.find_all('td')
                for index in range(0, len(th_list)):
                    
                    #print(th_list[index].text.strip().find('IOC ID:'))
                    if  th_list[index].text.strip().find('IOC Type') >= 0:
                        event.add("extra.ioc_type", td_list[index].text.strip())
                    if  th_list[index].text.strip().find('IOC ID:') >= 0:
                        event.add("extra.ioc_id", td_list[index].text.strip())
                    if  th_list[index].text.strip().find('Threat Type') >= 0:
                        event.add("extra.threat_type", td_list[index].text.strip())
                    if  th_list[index].text.strip().find('Malware alias:') >= 0:
                        event.add("extra.malware_alias", td_list[index].text.strip().split(", "))
                    if  th_list[index].text.strip().find('Confidence Level') >= 0:
                        event.add("extra.confidence_level", td_list[index].text.strip())
    
            self.logger.info("sucessfully added extra data")

            self.send_message(event)
        self.acknowledge_message()
    def check_ip(self, ip_addr: str) -> bool:
        IP_REGEX = '^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$'
        if re.search(IP_REGEX, ip_addr):
            return True
        else:
            return False
    def check_sha256(self, sha256: str) -> bool:
        if(len(sha256) == 64): return True
        return False
    def check_sha1(self, sha1: str) -> bool:
        if(len(sha1) == 40): return True
        return False
    def check_md5(self, md5: str) -> bool:
        if(len(md5) == 32): return True
        return False


BOT = AbusechThreatfoxParseBot
