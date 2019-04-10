# -*- coding: utf-8 -*-
"""
Testing AbusechZeuSExpertBot.
"""

import unittest
import json

import intelmq.lib.test as test
from intelmq.bots.experts.abusech.expert_zeus import AbusechZeuSExpertBot


EXAMPLE_INPUT = {'__type': 'Event',
                 'extra.status': 'offline',
                 'source.ip': '31.220.2.200'
                 }
EXAMPLE_OUTPUT = {'__type': 'Event',
                  'extra.status': 'offline',
                  'time.source': '2019-03-15T00:00:00+00:00',
                  'malware.hash.md5': 'c9bc32bd6fcbf7d1261aa5931d495f50',
                  'source.ip': '31.220.2.200',
                  'source.url': 'http://31.220.2.200/~bulbligh/j/panel/config.jpg'
                  }


class TestAbusechZeuSExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusechZeuSExpert.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AbusechZeuSExpertBot

    def test_event(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':
    unittest.main
