# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.precisionsec.parser import PrecisionsecParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_precisionsec.data')) as handle:
    REPORT_DATA = handle.read()

REPORT = {"__type": "Report",
          "feed.url": "https://precisionsec.com/threat-intelligence-feeds/agent-tesla",
          "raw": utils.base64_encode(REPORT_DATA),
          }

EVENT = {"__type": "Event",
         "feed.url": "https://precisionsec.com/threat-intelligence-feeds/agent-tesla",
         "malware.name": "agent-tesla",
         "classification.type": "malware",
         "source.url": "http://www.ryanmotors.co/banners/obm/obm.exe",
         "time.source": "2018-11-22T00:30:06+00:00",
         "raw": "PHRyPgo8dGQgc3R5bGU9InRleHQtYWxpZ246IGxlZnQ7IHdvcmQtd3JhcDpicmVhay13b3JkOyI+"
                "aHR0cDovL3d3dy5yeWFubW90b3JzLmNvL2Jhbm5lcnMvb2JtL29ibS5leGU8L3RkPgo8dGQgc3R5b"
                "GU9InRleHQtYWxpZ246IGxlZnQ7Ij4yMDE4LTExLTIyIDAwOjMwOjA2CjwvdGQ+CjwvdHI+"
         }


class TestPrecisionsecParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = PrecisionsecParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT)


if __name__ == '__main__':
    unittest.main
