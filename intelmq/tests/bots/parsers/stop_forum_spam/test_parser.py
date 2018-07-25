# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.stop_forum_spam.parser import StopForumSpamParserBot
from intelmq.lib import utils


with open(os.path.join(os.path.dirname(__file__), 'test_stop_forum_spam.data'), 'rb') as handle:
    REPORT_DATA = handle.read()

EXAMPLE_REPORT = {"feed.name": "StopForumSpam Feed",
                  "feed.provider": "stopforumspam.com",
                  "__type": "Report",
                  "raw": utils.base64_encode(REPORT_DATA),
                  "time.observation": "2018-07-03T12:19:24+00:00"
                  }

EXAMPLE_EVENT = {"__type": "Event",
                 "feed.name": "StopForumSpam Feed",
                 "feed.provider": "stopforumspam.com",
                 "time.observation": "2018-07-03T12:19:24+00:00",
                 'classification.type': 'spam',
                 'source.ip': '1.0.133.156',
                 'raw': 'MS4wLjEzMy4xNTY='
                 }


class TestStopForumSpamParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for StopForumSpamParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = StopForumSpamParserBot
        self.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
