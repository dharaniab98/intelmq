# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.mrlooquer.parser import MrlooquerParserBot

from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_mrlooquer.data')) as handle:
    REPORT_DATA = handle.read()

EXAMPLE_REPORT = {"feed.name": "Mrlooquer Feed",
                  "feed.url": "https://iocfeed.mrlooquer.com/feed.csv",
                  "raw": utils.base64_encode(REPORT_DATA),
                  "__type": "Report",
                  "time.observation": "2019-07-11T00:00:00+00:00"
                  }
EXAMPLE_EVENT = {"feed.name": "Mrlooquer Feed",
                 "feed.url": "https://iocfeed.mrlooquer.com/feed.csv",
                 "__type": "Event",
                 'classification.type': 'phishing',
                 'extra.destination_port': ['443', '32768', '8080', '80', '2049'],
                 'raw': 'WyIwMDBvd2FtYWlsMC4wMDB3ZWJob3N0YXBwLmNvbSIsICIxNDUuMTQuMTQ1LjE4'
                        'NyIsICIyMDQ5MTUiLCAiMCIsICJbNDQzLDMyNzY4LDgwODAsODAsMjA0OV0iLCAi'
                        'MmEwMjo0NzgwOmRlYWQ6NWM3MTo6MSIsICIyMDQ5MTUiLCAiMCIsICJbMzI3Njgs'
                        'MjA0OSw4MDgwLDQ0Myw4MCwzMjc2N10iLCAiMmEwMjo0NzgwOmRlYWQ6NWM3MTo6'
                        'IiwgImZyYXVkIiwgInBoaXNoaW5nIiwgImJ1bGtwaGlzaGluZyIsICJmYWxzZSIs'
                        'ICJ0cnVlIl0=',
                 'source.asn': 204915,
                 'source.fqdn': '000owamail0.000webhostapp.com',
                 'source.ip': '145.14.145.187'
                 }


class TestMrlooquerParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for MrlooquerParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = MrlooquerParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
