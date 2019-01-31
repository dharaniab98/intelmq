# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.feodotracker.expert import FeodoTrackerExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "feed.url": "https://feodotracker.abuse.ch/browse",
                 "feed.provider": "abuse.ch",
                 "time.observation": "2019-01-24T04:00:50+00:00",
                 "source.ip": "186.75.241.230",
                 "status": "Online",
                 "time.source": "2019-01-23T09:20:10+00:00",
                 "classification.type": "c&c",
                 "malware.name": "heodo",
                 "source.asn": 11556
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "feed.url": "https://feodotracker.abuse.ch/browse",
                  "feed.provider": "abuse.ch",
                  "time.observation": "2019-01-24T04:00:50+00:00",
                  "source.ip": "186.75.241.230",
                  "status": "Online",
                  "time.source": "2019-01-23T09:20:10+00:00",
                  "classification.type": "c&c",
                  "malware.name": "heodo",
                  "source.asn": 11556,
                  "destination.port": 80,
                  "malware.hash.md5": "8a831c8be1460a0da440b3b8c0087db5"
                  }


class TestFeodoTrackerExpertBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FeodoTrackerExpertBot

    def test_event(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(-1, EXAMPLE_OUTPUT)


if __name__ == '__main__':
    unittest.main
