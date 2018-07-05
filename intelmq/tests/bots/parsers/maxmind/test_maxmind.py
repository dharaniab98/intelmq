# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.maxmind.parser import MaxmindParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_maxmind.data')) as handle:
    REPORT_DATA = handle.read()

REPORT = {"__type": "Report",
          "feed.name": "maxmind feed",
          "feed.url": "https://www.maxmind.com/en/high-risk-ip-sample-list",
          "feed.provider": "maxmind.com",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-05-04T11:16:46+00:00"
          }
EVENT1 = {"feed.name": "maxmind feed",
          "feed.url": "https://www.maxmind.com/en/high-risk-ip-sample-list",
          "feed.provider": "maxmind.com",
          "time.observation": "2018-05-04T11:16:46+00:00",
          "__type": "Event",
          "classification.type": "blacklist",
          "source.ip": "1.40.215.65",
          "raw": "PGEgY2xhc3M9InNwYW4zIiBocmVmPSJoaWdoLXJpc2staXAtc2FtcGxlLzEuNDAuMjE1LjY1Ij4xLjQwLjIxNS42NTwvYT4="
          }


class TestMaxmindParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = MaxmindParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)


if __name__ == '__main__':
    unittest.main
