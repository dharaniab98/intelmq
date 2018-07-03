# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.cruzit.parser import CruzitParserBot
from intelmq.lib import utils


with open(os.path.join(os.path.dirname(__file__), 'test_cruzit.data'), 'rb') as handle:
    REPORT_DATA = handle.read()

EXAMPLE_REPORT = {"feed.url": "http://www.cruzit.com/xwbl2txt.php",
                  "feed.name": "Cruzit Feed",
                  "__type": "Report",
                  "raw": utils.base64_encode(REPORT_DATA),
                  "time.observation": "2018-07-03T09:15:13+00:00"
                  }

EXAMPLE_EVENT = {"__type": "Event",
                 "feed.url": "http://www.cruzit.com/xwbl2txt.php",
                 'classification.type': 'blacklist',
                 'feed.name': 'Cruzit Feed',
                 "time.observation": "2018-07-03T09:15:13+00:00",
                 'source.ip': '1.164.97.194',
                 'raw': 'MS4xNjQuOTcuMTk0',
                 }


class TestCruzitParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CruzitParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = CruzitParserBot
        self.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
