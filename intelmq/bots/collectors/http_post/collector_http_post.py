# -*- coding: utf-8 -*-
"""
HTTP post collector bot

Parameters:
http_url: string
http_header: dictionary
    default: {}
http_verify_cert: boolean
    default: True
extract_files: value used to extract files from downloaded compressed file
    default: None
    all: True; some: string with file names separated by ,
http_username, http_password: string
http_proxy, https_proxy: string
http_timeout_sec: tuple of two floats or float
http_timeout_max_tries: an integer depicting how often a connection attempt is retried
data: dictionary
    default: {}
"""
import json
import requests

from intelmq.lib.bot import CollectorBot



class HTTPPostCollectorBot(CollectorBot):

    def init(self):
        self.set_request_parameters()

    def process(self):
        http_url = self.parameters.http_url

        self.logger.info("started requesting %r.", http_url)

        timeoutretries = 0
        resp = None

        while timeoutretries < self.http_timeout_max_tries and resp is None:
            try:
                resp = requests.post(url=http_url, data= json.dumps(self.parameters.data), auth=self.auth,
                                     proxies=self.proxy, headers=self.http_header,
                                     verify=self.http_verify_cert,
                                     cert=self.ssl_client_cert,
                                     timeout=self.http_timeout_sec)

            except requests.exceptions.Timeout:
                timeoutretries += 1
                self.logger.warn("Timeout whilst getting the reponse.")

        if resp is None and timeoutretries >= self.http_timeout_max_tries:
            self.logger.error("Request timed out %i times in a row.",
                              timeoutretries)
            return

        if resp.status_code // 100 != 2:
            raise ValueError('HTTP response status code was %i.' % resp.status_code)

        self.logger.info("Request was sucessfull")
        report = self.new_report()
        report.add("raw", json.dumps(resp.json()))
        report.add("feed.url", http_url)
        self.send_message(report)
        self.logger.info("Message was sent sucessfull")

BOT = HTTPPostCollectorBot