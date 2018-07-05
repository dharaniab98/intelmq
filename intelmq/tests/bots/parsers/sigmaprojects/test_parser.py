# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.sigmaprojects.parser import SigmaProjectsParserBot
from intelmq.lib import utils


with open(os.path.join(os.path.dirname(__file__), 'test_sigmaprojects.data'), 'rb') as handle:
    REPORT_DATA = handle.read()

EXAMPLE_REPORT = {"feed.name": "SigmaProjects Feed",
                  "feed.url": "https://blocklist.sigmaprojects.org/api.cfc?method=getlist&lists=drop,zeus,spyware",
                  "feed.provider": "SigmaProjects",
                  "__type": "Report",
                  "raw": utils.base64_encode(REPORT_DATA),
                  "time.observation": "2018-07-02T07:42:57+00:00",
                  }

EXAMPLE_EVENT = [{"__type": "Event",
                  "feed.name": "SigmaProjects Feed",
                  "feed.provider": "SigmaProjects",
                  "feed.url": "https://blocklist.sigmaprojects.org/api.cfc?method=getlist&lists=drop,zeus,spyware",
                  "classification.type": "blacklist",
                  "time.observation": "2018-07-02T07:42:57+00:00",
                  'source.network': '1.10.16.0/20',
                  'raw': 'MS4xMC4xNi4wLzIw'
                  },
                 {"__type": "Event",
                  "feed.name": "SigmaProjects Feed",
                  "feed.provider": "SigmaProjects",
                  "feed.url": "https://blocklist.sigmaprojects.org/api.cfc?method=getlist&lists=drop,zeus,spyware",
                  "classification.type": "blacklist",
                  "time.observation": "2018-07-02T07:42:57+00:00",
                  'source.network': '1.32.128.0/18',
                  'raw': 'MS4zMi4xMjguMC8xOA==',
                  }]


class TestSigmaProjectsParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for SigmaProjectsParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = SigmaProjectsParserBot
        self.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT[0])
        self.assertMessageEqual(1, EXAMPLE_EVENT[1])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
