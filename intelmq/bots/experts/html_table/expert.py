# -*- coding: utf-8 -*-
"""
HTML Table Expert

Parameters:
url_format: string
url_param: string
columns: string
ignore_values: string
skip_table_head: boolean
attribute_name: string
attribute_value: string
table_index: int
split_column: string
split_separator: string
split_index: int
"""

import requests
from bs4 import BeautifulSoup as bs
from dateutil.parser import parse

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import InvalidArgument
from intelmq.lib.harmonization import DateTime

TIME_CONVERSIONS = {'timestamp': DateTime.from_timestamp,
                    'windows_nt': DateTime.from_windows_nt,
                    'epoch_millis': DateTime.from_epoch_millis,
                    None: lambda value: parse(value, fuzzy=True).isoformat() + " UTC"}


class HTMLTableExpertBot(Bot):

    def init(self):
        self.set_request_parameters()
        self.url_param = self.parameters.url_param
        self.columns = self.parameters.columns

        # convert columns to an array
        if type(self.columns) is str:
            self.columns = [column.strip() for column in self.columns.split(",")]
        self.ignore_values = getattr(self.parameters, "ignore_values", len(self.columns) * [''])
        if type(self.ignore_values) is str:
            self.ignore_values = [value.strip() for value in self.ignore_values.split(",")]

        self.table_index = getattr(self.parameters, "table_index", 0)
        self.attr_name = getattr(self.parameters, "attribute_name", None)
        self.attr_value = getattr(self.parameters, "attribute_value", None)

        self.skip_head = getattr(self.parameters, "skip_table_head", True)
        self.skip_row = 1 if self.skip_head else 0
        self.split_column = getattr(self.parameters, "split_column", None)
        self.split_separator = getattr(self.parameters, "split_separator", None)
        self.split_index = getattr(self.parameters, "split_index", 0)
        self.time_format = getattr(self.parameters, "time_format", None)
        if self.time_format not in TIME_CONVERSIONS.keys():
            raise InvalidArgument('time_format', got=self.time_format,
                                  expected=list(TIME_CONVERSIONS.keys()),
                                  docs='docs/Bots.md')

    def process(self):
        event = self.receive_message()
        url_param = self.url_param.split('|') if '|' in self.url_param else [self.url_param, ]
        for param in url_param:
            if(event.get(param)):
                url = self.parameters.url_format % (event[param])
                break

        timeoutretries = 0
        resp = None

        while timeoutretries < self.http_timeout_max_tries and resp is None:
            try:
                resp = requests.get(url=url, auth=self.auth,
                                    proxies=self.proxy, headers=self.http_header,
                                    verify=self.http_verify_cert,
                                    cert=self.ssl_client_cert,
                                    timeout=self.http_timeout_sec)

            except requests.exceptions.Timeout:
                timeoutretries += 1
                self.logger.warn("Timeout whilst downloading the report.")

        if resp is None and timeoutretries >= self.http_timeout_max_tries:
            self.logger.error("Request timed out %i times in a row.",
                              timeoutretries)
            return

        if resp.status_code // 100 != 2:
            raise ValueError('HTTP response status code was %i.' % resp.status_code)

        soup = bs(resp.text, 'html.parser')
        if self.attr_name is not None:
            table = soup.find_all('table', attrs={self.attr_name: self.attr_value})
        else:
            table = soup.find_all('table')

        if len(table) > self.table_index:
            table = table[self.table_index]
            row = table.find_all('tr')[self.skip_row:]

            for feed in row:

                tdata = [data.text for data in feed.find_all('td')]

                for key, data, ignore_value in zip(self.columns, tdata, self.ignore_values):
                    keys = key.split('|') if '|' in key else [key, ]
                    data = data.strip()
                    if data == ignore_value:
                        continue
                    for key in keys:
                        if isinstance(data, str) and not data:  # empty string is never valid
                            break

                        if key in ["__IGNORE__", ""]:
                            break

                        if self.split_column and key == self.split_column:
                            data = data.split(self.split_separator)[int(self.split_index)]
                            data = data.strip()

                        if key in ["time.source", "time.destination"]:
                            try:
                                data = int(data)
                            except:
                                pass
                            data = TIME_CONVERSIONS[self.time_format](data)

                        elif key.endswith('.url'):
                            if not data:
                                continue
                            if '://' not in data:
                                data = self.parameters.default_url_protocol + data

                        if event.add(key, data, overwrite=True, raise_failure=False):
                            break

                self.send_message(event)
        else:
            self.send_message(event)
        self.acknowledge_message()


BOT = HTMLTableExpertBot
