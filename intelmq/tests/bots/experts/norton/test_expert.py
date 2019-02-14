# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.norton.expert import NortonExpertBot

EXAMPLE_INPUT1 = {"__type": "Event",
                  "feed.url": "https://safeweb.norton.com/buzz",
                  "time.observation": "2019-01-19T09:18:44+00:00",
                  "source.fqdn": "uk-obninsk.ru",
                  "classification.type": "malware"
                  }

EXAMPLE_INPUT2 = {"__type": "Event",
                  "feed.url": "https://safeweb.norton.com/buzz",
                  "time.observation": "2019-01-19T09:18:44+00:00",
                  "source.ip": "159.89.120.246",
                  "classification.type": "malware"
                  }

EXAMPLE_OUTPUT1 = {"__type": "Event",
                   "feed.url": "https://safeweb.norton.com/buzz",
                   "time.observation": "2019-01-19T09:18:44+00:00",
                   "source.fqdn": "uk-obninsk.ru",
                   "classification.type": "malware",
                   "extra.threat_info": "Web Attack: Mass Injection Website 19",
                   "source.url": "http://www.uk-obninsk.ru/media/system/js/mootools.js"
                   }

EXAMPLE_OUTPUT2 = {"__type": "Event",
                   "feed.url": "https://safeweb.norton.com/buzz",
                   "time.observation": "2019-01-19T09:18:44+00:00",
                   "source.ip": "159.89.120.246",
                   "classification.type": "malware",
                   "extra.threat_info": "Web Attack: Fake Tech Support Website 36",
                   "feed.url": "https://safeweb.norton.com/buzz",
                   "source.url": "http://159.89.120.246/"
                   }


class TestNortonExpertBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = NortonExpertBot

    def test_event_with_fqdn(self):
        self.input_message = EXAMPLE_INPUT1
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT1)

    def test_event_with_ip(self):
        self.input_message = EXAMPLE_INPUT2
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT2)


if __name__ == '__main__':
    unittest.main
