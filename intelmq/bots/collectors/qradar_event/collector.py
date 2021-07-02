# -*- coding: utf-8 -*-
"""
QRADAR collector bot

Parameters:
qradar_host: string
aql_query: string
http_header: dictionary
    default: {}
http_verify_cert: boolean
    default: True
http_username, http_password: string
http_proxy, https_proxy: string
http_timeout_sec: tuple of two floats or float
http_timeout_max_tries: an integer depicting how often a connection attempt is retried
"""
import json
import time
import requests

from intelmq.lib.bot import CollectorBot


class QradarEventCollectorBot(CollectorBot):

    def init(self):
        self.set_request_parameters()
        self.qradar_host = self.parameters.qradar_host
        self.aql_query = self.parameters.aql_query

    def query_result(self):

        TIMER = 5

        while True:
            try:
                resp = requests.get(url="%s/api/ariel/searches/%s" % (self.qradar_host, self.search_id),
                                    auth=self.auth, proxies=self.proxy, headers=self.http_header,
                                    verify=self.http_verify_cert, cert=self.ssl_client_cert,
                                    timeout=self.http_timeout_sec)

                if resp.status_code // 100 != 2:
                    raise ValueError('HTTP response status code was %i.' % resp.status_code)

                resp_json = resp.json()
                if resp_json.get("status", None) == "COMPLETED":
                    self.logger.info("Obtained Return Object.")
                    break

                else:
                    self.logger.info("Query completion: [%s%%] Timer: [%s]" % (resp_json.get('progress'), TIMER))

            except Exception as e:
                self.logger.info("Exception during finding query: \n %s" % e)

            finally:
                time.sleep(TIMER)
                TIMER = TIMER + 5

                if TIMER >= 50:
                    self.logger.error("No Result Returned")
                    return False

        timeoutretries = 0

        while timeoutretries < self.http_timeout_max_tries:
            try:
                resp = requests.get(url="%s/api/ariel/searches/%s/results" % (self.qradar_host, self.search_id),
                                    auth=self.auth, proxies=self.proxy, headers=self.http_header,
                                    verify=self.http_verify_cert, cert=self.ssl_client_cert,
                                    timeout=self.http_timeout_sec)
            except requests.exceptions.Timeout:
                timeoutretries += 1
                self.logger.warn("Timeout whilst accessing AQL result")

            if resp.status_code // 100 != 2:
                raise ValueError('HTTP response status code was %i.' % resp.status_code)

            resp_json = resp.json()
            return resp_json

    def run_query(self):

        timeoutretries = 0

        while timeoutretries < self.http_timeout_max_tries:
            try:
                resp = requests.post(url="%s/api/ariel/searches" % (self.qradar_host),
                                     params={"query_expression": self.aql_query},
                                     proxies=self.proxy, headers=self.http_header,
                                     verify=self.http_verify_cert,
                                     cert=self.ssl_client_cert,
                                     timeout=self.http_timeout_sec)
            except requests.exceptions.Timeout:
                timeoutretries += 1
                self.logger.warn("Timeout whilst accessing AQL result")

            if resp.status_code // 100 != 2:
                raise ValueError('HTTP response status code was %i.' % resp.status_code)

            resp_json = resp.json()
            search_id = resp_json["search_id"]
            return search_id

    def process(self):

        self.logger.info("Running AQL: ", self.parameters.aql_query)

        self.search_id = self.run_query()

        if self.search_id:
            return_list = self.query_result()

        if return_list and type(return_list) is dict:
            raw_report = json.dumps(return_list)

            self.logger.info("Qradar AQL Query Completed.")

            report = self.new_report()
            report.add("raw", raw_report)
            report.add("feed.url", self.parameters.qradar_host)
            self.send_message(report)


BOT = QradarEventCollectorBot
