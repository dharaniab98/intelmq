# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.honeypot.parser import HoneypotParserBot
from intelmq.lib import utils


with open(os.path.join(os.path.dirname(__file__), 'test_honeypot.data'), 'rb') as handle:
    REPORT_DATA = handle.read()

EXAMPLE_REPORT = {"feed.url": "https://www.projecthoneypot.org/list_of_ips.php",
                  "feed.name": "Honeypot Feed",
                  "__type": "Report",
                  "raw": utils.base64_encode(REPORT_DATA),
                  "time.observation": "2018-06-30T08:59:52+00:00"
                  }

EXAMPLE_EVENT = {"__type": "Event",
                 'classification.type': 'blacklist',
                 'extra.event': 'Bad Event',
                 'extra.last_seen': '2018-06-29',
                 'feed.name': 'Honeypot Feed',
                 'feed.url': 'https://www.projecthoneypot.org/list_of_ips.php',
                 'raw': 'PHRyIGNsYXNzPSJteHJlIj4KPHRkIG5vd3JhcD0iIj48YSBocmVmPSIvbGlzdF9vZl9pc'
                        'HMucGhwP2N0cnk9dXMiPjxpbWcgc3JjPSIvaW1hZ2VzL2ZsYWdzL3VzLnBuZyIgdGl0bG'
                        'U9IiIvPjwvYT7CoDxhIGNsYXNzPSJibm9uZSIgaHJlZj0iL2lwXzUwLjE3LjE3Ny4yMzA'
                        'iPjUwLjE3LjE3Ny4yMzA8L2E+wqB8wqBDPC90ZD4KPHRkIGFsaWduPSJyaWdodCIgbm93'
                        'cmFwPSIiPkJhZCBFdmVudDwvdGQ+Cjx0ZCBhbGlnbj0icmlnaHQiPjE8L3RkPgo8dGQgY'
                        'WxpZ249InJpZ2h0Ij4NDQogICAgICAgICAgICAJCTIwMTgtMDYtMjnCoA0NCiAgICAgIC'
                        'AgICAgIAk8L3RkPgo8dGQgYWxpZ249InJpZ2h0Ij4NDQogICAgICAgICAgICAJCTIwMTg'
                        'tMDYtMjnCoA0NCiAgICAgICAgICAgIAk8L3RkPgo8L3RyPg==',
                 'source.ip': '50.17.177.230',
                 'time.source': '2018-06-29T00:00:00+00:00'
                 }


class TestHoneypotParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for HoneypotParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = HoneypotParserBot
        self.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(1, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
