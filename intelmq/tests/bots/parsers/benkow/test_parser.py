# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.benkow.parser import BenkowParserBot
from intelmq.lib import utils


with open(os.path.join(os.path.dirname(__file__), 'test_benkow.data'), 'rb') as handle:
    REPORT_DATA = handle.read()

EXAMPLE_REPORT = {"feed.url": "http://benkow.cc/export.php",
                  "feed.name": "Benkow Feed",
                  "__type": "Report",
                  "raw": utils.base64_encode(REPORT_DATA),
                  "time.observation": "2018-06-28T08:11:43+00:00"
                  }

EXAMPLE_EVENT = [{"__type": "Event",
                  'feed.name': 'Benkow Feed',
                  'feed.url': 'http://benkow.cc/export.php',
                  "classification.type": "malware",
                  'malware.name': 'pony',
                  'source.ip': '103.63.2.250',
                  'source.url': 'http://www.faridatiannery.com/panel/admin.php',
                  'time.source': '2017-08-26T00:00:00+00:00',
                  'raw': 'IjEiOyJwb255IjsiaHR0cDovL3d3dy5mYXJpZGF0aWFubmVyeS5jb20vcGFuZWwvY'
                         'WRtaW4ucGhwIjsiMTAzLjYzLjIuMjUwIjsiMjYtMDgtMjAxNyI7',
                  },
                 {"__type": "Event",
                  'feed.name': 'Benkow Feed',
                  'feed.url': 'http://benkow.cc/export.php',
                  "classification.type": "malware",
                  'malware.name': 'zeus fork',
                  'source.url': 'http://hutrnadhi.com/off/www.php?m=login',
                  'source.ip': '119.28.43.178',
                  'time.source': '2017-08-26T00:00:00+00:00',
                  'raw': 'IjIiOyJaZXVzIGZvcmsiOyJodHRwOi8vaHV0cm5hZGhpLmNvbS9vZmYvd3d3LnBocD9'
                         'tPWxvZ2luIjsiMTE5LjI4LjQzLjE3OCI7IjI2LTA4LTIwMTciOw==',
                  }]


class TestBenkowParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for BenkowParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = BenkowParserBot
        self.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT[0])
        self.assertMessageEqual(1, EXAMPLE_EVENT[1])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
