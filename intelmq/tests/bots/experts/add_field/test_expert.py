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

EXAMPLE_INPUT3 = {"__type": "Event",
                  "classification.type": "malware",
                  "time.observation": "2018-07-27T00:00:00+00:00",
                  "extra.last_seen": "2018-07-26T00:00:00+00:00",
                  "extra.tags": "malware",
                  "feed.name": "test-feed-3"}

EXAMPLE_INPUT4 = {"__type": "Event",
                  "classification.type": "malware",
                  "time.observation": "2018-07-27T00:00:00+00:00",
                  "extra.tags": "malware",
                  "feed.name": "test-feed-4"}

EXAMPLE_INPUT5 = {"__type": "Event",
                  "classification.type": "malware",
                  "extra.tags": "None",
                  "extra.urlhaus.threat_type": "malware_download",
                  "extra.urlhause_link": "https://urlhaus.abuse.ch/url/122336/",
                  "feed.accuracy": 100.0,
                  "feed.name": "urlhaus",
                  "feed.provider": "abuse.ch",
                  "feed.url": "https://urlhaus.abuse.ch/downloads/csv/",
                  "source.url": "http://mat-bansgh.com/DE/YZFCRSAWKE1998409/Bestellungen/RECH/",
                  "status": "online",
                  "time.observation": "2019-02-12T10:43:47+00:00",
                  "time.source": "2019-02-12T10:33:05+00:00"}

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

EXAMPLE_OUTPUT3 = {'__type': 'Event',
                   'classification.type': 'malware',
                   'time.observation': '2018-07-27T00:00:00+00:00',
                   'extra.last_seen': '2018-07-26T00:00:00+00:00',
                   'extra.author': 'cert-in',
                   'extra.tags': 'malware',
                   'feed.name': 'test-feed-3'}

EXAMPLE_OUTPUT4 = {"__type": "Event",
                   "classification.type": "malware",
                   "time.observation": "2018-07-27T00:00:00+00:00",
                   "malware.name": "zeus",
                   "extra.tags": "malware",
                   "feed.name": "test-feed-4"}

EXAMPLE_OUTPUT5 = {"__type": "Event",
                   "classification.type": "malware",
                   "extra.tags": "None",
                   "extra.urlhaus.threat_type": "malware_download",
                   "extra.urlhause_link": "https://urlhaus.abuse.ch/url/122336/",
                   "feed.accuracy": 100.0,
                   "feed.name": "urlhaus",
                   "feed.provider": "abuse.ch",
                   "feed.url": "https://urlhaus.abuse.ch/downloads/csv/",
                   "source.url": "http://mat-bansgh.com/DE/YZFCRSAWKE1998409/Bestellungen/RECH/",
                   "status": "online",
                   "time.observation": "2019-02-12T10:43:47+00:00",
                   "time.source": "2019-02-12T10:33:05+00:00",
                   "extra.new_feed": "yes"}


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

    def test_event_with_extra_dict(self):
        self.input_message = EXAMPLE_INPUT3
        self.sysconfig = {'field-name': 'author', 'field-value': 'cert-in'}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT3)

    def test_event_not_add_to_extra(self):
        self.input_message = EXAMPLE_INPUT4
        self.sysconfig = {'field-name': 'malware.name', 'field-value': 'zeus', 'add_to_extra': False}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT4)

    def test_event_extra_mapping(self):
        self.input_message = EXAMPLE_INPUT5
        self.sysconfig = {'field-name': 'new_feed', 'field-value': 'yes', 'add_to_extra': True}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT5)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
