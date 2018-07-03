# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.botscout.parser import BotscoutParserBot
from intelmq.lib import utils


with open(os.path.join(os.path.dirname(__file__), 'test_botscout.data'), 'rb') as handle:
    REPORT_DATA = handle.read()

EXAMPLE_REPORT = {"feed.url": "http://botscout.com/last_caught_cache.txt",
                  "feed.name": "Botscout Feed",
                  "__type": "Report",
                  "raw": utils.base64_encode(REPORT_DATA),
                  "time.observation": "2018-07-03T11:43:15+00:00"
                  }

EXAMPLE_EVENT = {"__type": "Event",
                 "feed.url": "http://botscout.com/last_caught_cache.txt",
                 "feed.name": "Botscout Feed",
                 "time.observation": "2018-07-03T11:43:15+00:00",
                 'classification.type': 'spam',
                 'source.account': 'faustschukin649638@mail.ru',
                 'source.ip': '217.30.64.26',
                 'raw': 'Um9uYWxkR2VyLGZhdXN0c2NodWtpbjY0OTYzOEBtYWlsLnJ1LDIxNy4zMC42NC4yNg=='
                 }


class TestBotscoutParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for BotscoutParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = BotscoutParserBot
        self.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
