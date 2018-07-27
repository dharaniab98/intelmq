# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.benkow_rat.parser import BenkowRATParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_benkow_rat.data')) as handle:
    REPORT_DATA = handle.read()

REPORT = {"__type": "Report",
          "feed.name": "URL",
          "feed.url": "http://benkow.cc/ratracker.php?page=1",
          "feed.provider": "benkow.cc",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-07-27T10:42:13+00:00"
          }

EVENT1 = {"feed.name": "URL",
          "feed.url": "http://benkow.cc/ratracker.php?page=1",
          "feed.provider": "benkow.cc",
          'source.url': "http://181.52.105.187:1996",
          "time.observation": "2018-07-27T10:42:13+00:00",
          "time.source": "2018-07-26T00:00:00+00:00",
          "__type": "Event",
          'malware.name': 'limerat',
          "classification.type": "malware",
          "source.ip": "181.52.105.187",
          "raw": "PHRyPjx0ZD48aW5wdXQgbmFtZT0ic2VsZWN0aW9uW10iIHR5cGU9ImNoZWNrYm94IiB2YWx1ZT"
                 "0iZnVjayIvPjwvdGQ+PHRkPjI2LTA3LTIwMTg8L3RkPjx0ZD5MaW1lUmF0PC90ZD48dGQ+MTgxL"
                 "jUyLjEwNS4xODc6MTk5NjwvdGQ+PHRkPjE4MS41Mi4xMDUuMTg3PC90ZD4gPC90cj4="
          }


class TestBenkowRATParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = BenkowRATParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)


if __name__ == '__main__':
    unittest.main
