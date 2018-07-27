# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.urlvir_ip.parser import URLVirIPParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_urlvir_ip.data')) as handle:
    REPORT_DATA = handle.read()

REPORT = {"__type": "Report",
          "feed.name": "URL",
          "feed.url": "http://www.urlvir.com/",
          "feed.provider": "urlvir.com",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-07-26T10:06:44+00:00"
          }

EVENT1 = {"feed.name": "URL",
          "feed.url": "http://www.urlvir.com/",
          "feed.provider": "urlvir.com",
          "time.observation": "2018-07-26T10:06:44+00:00",
          "time.source": "2018-07-25T00:00:00+00:00",
          "__type": "Event",
          'malware.hash.md5': '71041a599486244406024590c5c5f51d',
          "classification.type": "malware",
          "source.ip": "169.239.217.12",
          "raw": "PHRyPjx0ZD4yMDE4LTA3LTI1PC90ZD4gPHRkPmh0dHA6Ly9iaXpidWlsZGVyLmNvLnphL25ld3NsZS4uLjwvdGQ+I"
                 "Dx0ZD4xNjkuMjM5LjIxNy4xMjwvdGQ+IDx0ZD43MTA0MWE1OTk0ODYyNDQ0MDYwMjQ1OTBjNWM1ZjUxZDwvdGQ+ID"
                 "x0ZD4zODEuMTEgS0I8L3RkPiA8dGQ+PGZvbnQgY29sb3I9InJlZCI+T05MSU5FPC9mb250PjwvdGQ+IDwvdHI+"
          }


class TestURLVirIPParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = URLVirIPParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)


if __name__ == '__main__':
    unittest.main
