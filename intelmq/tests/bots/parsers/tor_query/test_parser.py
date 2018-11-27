# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.tor_query.parser import TorQueryParserBot
from intelmq.lib import utils


with open(os.path.join(os.path.dirname(__file__), 'test_tor_query.data'), 'rb') as handle:
    REPORT_DATA = handle.read()

EXAMPLE_REPORT = {"feed.url": "http://torstatus.blutmagie.de/query_export.php/Tor_query_EXPORT.csv",
                  "feed.name": "Tor Network Status Project Query Feed",
                  "__type": "Report",
                  "raw": utils.base64_encode(REPORT_DATA)
                  }

EXAMPLE_EVENT = {"__type": "Event",
                 'classification.type': 'tor',
                 'extra.tor_flags': ['Fast', 'Stable', 'Running', 'Valid', 'V2Dir'],
                 'feed.name': 'Tor Network Status Project Query Feed',
                 'feed.url': 'http://torstatus.blutmagie.de/query_export.php/Tor_query_EXPORT.csv',
                 'raw': 'MDAwMFVzZXJ6YXAsREUsNjAsMjcxLDQ2LjM4LjI1MC4zOSx0aHJlZXB3b29kLnVzZXJ6YXAuZGUsOTAwMSw'
                        '5MDMwLDAsMCwxLDAsMCwxLDEsMSwxLFRvciAwLjMuNC45IG9uIExpbnV4LDAsMCwyMDEzLTExLTIzLE5FVE'
                        'NVUC1BUyBuZXRjdXAgR21iSC0gREUsMTk3NTQwLDIyMyxbMjAwMTo0NzA6NTI2MDo6MV06OTAwMQ==',
                 'source.ip': '46.38.250.39'}


class TestTorQueryParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for TorQueryParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = TorQueryParserBot
        self.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(1, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
