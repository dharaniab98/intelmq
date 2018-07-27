# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.add_field.expert import AddFieldExpertBot

EXAMPLE_INPUT1 = {"__type": "Event",
                  "classification.type": "malware",
                  "time.observation": "2018-07-27T00:00:00+00:00",
                  "feed.name": "test-feed-1"}

EXAMPLE_INPUT2 = {"__type": "Event",
                  "classification.type": "malware",
                  "time.observation": "2018-07-27T00:00:00+00:00",
                  "extra.last_seen": "2018-07-26T00:00:00+00:00",
                  "feed.name": "test-feed-2"}

EXAMPLE_OUTPUT1 = {'__type': 'Event',
                   'classification.type': 'malware',
                   'time.observation': '2018-07-27T00:00:00+00:00',
                   'extra.author': 'tls',
                   'feed.name': 'test-feed-1'}

EXAMPLE_OUTPUT2 = {'__type': 'Event',
                   'classification.type': 'malware',
                   'time.observation': '2018-07-27T00:00:00+00:00',
                   'extra.last_seen': '2018-07-26T00:00:00+00:00',
                   'extra.author': 'cert',
                   'feed.name': 'test-feed-2'}


class TestAddFieldExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AddFieldExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AddFieldExpertBot

    def test_event_without_extra(self):
        self.input_message = EXAMPLE_INPUT1
        self.sysconfig = {'field-name': 'author', 'field-value': 'tls'}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT1)

    def test_event_with_extra(self):
        self.input_message = EXAMPLE_INPUT2
        self.sysconfig = {'field-name': 'author', 'field-value': 'cert'}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
