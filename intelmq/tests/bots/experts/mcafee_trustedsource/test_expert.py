# -*- coding: utf-8 -*-
"""
Testing McafeeTrustedSourceExpertBot.
"""

import unittest
import json

from pkg_resources import resource_filename

import intelmq.lib.test as test
from intelmq.lib.utils import load_configuration
from intelmq.bots.experts.mcafee_trustedsource.expert import McafeeTrustedSourceExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "feed.accuracy": 100.0,
                 "feed.name": "URL",
                 "feed.provider": "abuse.ch",
                 "feed.url": "https://urlhaus.abuse.ch/downloads/csv/",
                 "time.observation": "2019-03-18T14:19:51+00:00",
                 "time.source": "2019-03-18T13:03:09+00:00",
                 "source.url": "http://107.172.41.9/assailant.arm6",
                 "status": "online",
                 "extra.urlhaus.threat_type": "malware_download",
                 "extra.tags": "bashlite,elf,gafgyt",
                 "extra.urlhaus_link": "https://urlhaus.abuse.ch/url/161367/",
                 "raw": "MTYxMzY3LDIwMTktMDMtMTggMTM6MDM6MDksaHR0cDovLzEwNy4xNzIuNDEuOS9hc3NhaWxhbnQuYXJtNixvbmxpbmUsbWFs"
                        "d2FyZV9kb3dubG9hZCwiYmFzaGxpdGUsZWxmLGdhZmd5dCIsaHR0cHM6Ly91cmxoYXVzLmFidXNlLmNoL3VybC8xNjEzNjcvDQo="}
EXAMPLE_OUTPUT = {"__type": "Event",
                  "feed.accuracy": 100.0,
                  "feed.name": "URL",
                  "feed.provider": "abuse.ch",
                  "feed.url": "https://urlhaus.abuse.ch/downloads/csv/",
                  "time.observation": "2019-03-18T14:19:51+00:00",
                  "time.source": "2019-03-18T13:03:09+00:00",
                  "source.url": "http://107.172.41.9/assailant.arm6",
                  "status": "online",
                  "extra.urlhaus.threat_type": "malware_download",
                  "extra.tags": "bashlite,elf,gafgyt",
                  "extra.urlhaus_link": "https://urlhaus.abuse.ch/url/161367/",
                  "raw": "MTYxMzY3LDIwMTktMDMtMTggMTM6MDM6MDksaHR0cDovLzEwNy4xNzIuNDEuOS9hc3NhaWxhbnQuYXJtNixvbmxpbmUsbWFsd"
                         "2FyZV9kb3dubG9hZCwiYmFzaGxpdGUsZWxmLGdhZmd5dCIsaHR0cHM6Ly91cmxoYXVzLmFidXNlLmNoL3VybC8xNjEzNjcvDQo=",
                  'extra.mcafee_categorization': 'Malicious Sites',
                  'extra.mcafee_reputation': 'High Risk'}


class TestMcafeeTrustedSourceExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for McafeeTrustedSourceExpert.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = McafeeTrustedSourceExpertBot

    def test_event(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':
    unittest.main
