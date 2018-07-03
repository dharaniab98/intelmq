# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.cedia.parser import CediaParserBot
from intelmq.lib import utils


with open(os.path.join(os.path.dirname(__file__), 'test_cedia.data'), 'rb') as handle:
    REPORT_DATA = handle.read()

EXAMPLE_REPORT = {"feed.url": "https://mirror.cedia.org.ec/malwaredomains/justdomains",
                  "feed.name": "Cedia Feed",
                  "__type": "Report",
                  "raw": utils.base64_encode(REPORT_DATA),
                  "time.observation": "2018-07-02T13:06:35+00:00"
                  }

EXAMPLE_EVENT = {"__type": "Event",
                 "feed.url": "https://mirror.cedia.org.ec/malwaredomains/justdomains",
                 "feed.name": "Cedia Feed",
                 "time.observation": "2018-07-02T13:06:35+00:00",
                 'classification.type': 'blacklist',
                 'source.fqdn': 'amazon.co.uk.security-check.ga',
                 'raw': 'YW1hem9uLmNvLnVrLnNlY3VyaXR5LWNoZWNrLmdh',
                 }


class TestCediaParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CediaParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = CediaParserBot
        self.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
