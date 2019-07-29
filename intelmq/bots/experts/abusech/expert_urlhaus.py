# -*- coding: utf-8 -*-

import json
import requests

from intelmq.lib.bot import Bot


class AbusechURLhausExpertBot(Bot):
    def init(self):
        self.set_request_parameters()

    def process(self):
        event = self.receive_message()
        post_url = "https://urlhaus-api.abuse.ch/v1/url/"
        url = event.get("source.url")
        data = {"url": url}

        timeoutretries = 0
        resp = None

        while timeoutretries < self.http_timeout_max_tries and resp is None:
            try:
                resp = requests.post(url=post_url, data=data, auth=self.auth,
                                     proxies=self.proxy, headers=self.http_header,
                                     verify=self.http_verify_cert,
                                     cert=self.ssl_client_cert,
                                     timeout=self.http_timeout_sec)

            except requests.exceptions.Timeout:
                timeoutretries += 1

        if not resp and resp.status_code // 100 != 2:
            self.send_message(event)

        res_data = json.loads(resp.text)
        if res_data['payloads']:
            for data in res_data['payloads']:
                new_event = event.copy()
                new_event.add('extra.file_name', data['filename'])
                new_event.add('extra.file_type', data['file_type'])
                new_event.add('malware.hash.md5', data['response_md5'])
                new_event.add('malware.hash.sha256', data['response_sha256'])
                if data['virustotal']:
                    new_event.add('extra.VT_status', data['virustotal']['result'])
                    new_event.add('extra.VT_link', data['virustotal']['link'])

                self.send_message(new_event)
        else:
            self.send_message(event)

        self.acknowledge_message()


BOT = AbusechURLhausExpertBot
