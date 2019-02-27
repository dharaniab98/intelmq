# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.utils as utils
import intelmq.lib.test as test
from intelmq.bots.experts.html_table.expert import HTMLTableExpertBot

EXAMPLE_INPUT = {"feed.name": "HTML Table Feed",
                 "feed.url": "https://feodotracker.abuse.ch/browse",
                 "__type": "Event",
                 "time.source": "2019-02-06T10:36:27+00:00",
                 "malware.name": "heodo",
                 "classification.type": "malware",
                 "source.ip": "201.192.163.160",
                 "status": "Offline",
                 "time.observation": "2019-01-01T00:00:00+00:00",
                 }

EXAMPLE_OUTPUT = EXAMPLE_INPUT.copy()
EXAMPLE_OUTPUT["malware.hash.md5"] = "112d95996a3df029beacf70c91863032"
EXAMPLE_OUTPUT["time.source"] = "2019-01-29T01:37:06+00:00"
EXAMPLE_OUTPUT["destination.port"] = 143

EXAMPLE_INPUT1 = {"__type": "Event",
                  "classification.type": "malware",
                  "extra.tags": "exe",
                  "extra.urlhaus.threat_type": "malware_download",
                  "extra.urlhause_link": "https://urlhaus.abuse.ch/url/145185/",
                  "feed.name": "urlhaus",
                  "feed.provider": "abuse.ch",
                  "feed.url": "https://urlhaus.abuse.ch/downloads/csv/",
                  "source.url": "http://fileservice.ga/POs.exe",
                  "status": "online",
                  "time.observation": "2019-02-25T07:40:51+00:00",
                  "time.source": "2019-02-25T07:11:09+00:00"
                  }
EXAMPLE_OUTPUT1 = EXAMPLE_INPUT1.copy()
EXAMPLE_OUTPUT1["malware.hash.sha256"] = "4474dd137a0fa4d69d8896131fc0ad04ff879eb5631dfcd38050937157e7487b"


class TestHTMLTableExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a HTMLTableExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HTMLTableExpertBot

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.input_message = EXAMPLE_INPUT
        self.sysconfig = {"url_format": "https://feodotracker.abuse.ch/browse/host/%s",
                          "url_param": "source.ip",
                          "columns": ["time.source", "malware.hash.md5", "__IGNORE__",
                                      "__IGNORE__", "destination.port"],
                          "table_index": 1,
                          "skip_head": True}
        self.run_bot()
        self.assertMessageEqual(-1, EXAMPLE_OUTPUT)

    def test_event1(self):
        """ Test if correct Event has been produced. """
        self.input_message = EXAMPLE_INPUT1
        self.sysconfig = {"url_format": "%s",
                          "url_param": "extra.urlhause_link",
                          "columns": ["__IGNORE__", "extra.file_name",
                                      "__IGNORE__", "malware.hash.sha256"],
                          "ignore_values": ["", "n/a", "", ""],
                          "table_index": 1,
                          "skip_head": True}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT1)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
