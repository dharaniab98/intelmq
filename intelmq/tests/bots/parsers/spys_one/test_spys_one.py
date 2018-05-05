# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.spys_one.parser import SpysOneParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_spys_one.data')) as handle:
    REPORT_DATA = handle.read()

REPORT = {"__type": "Report",
          "feed.name": "spys one feed",
          "feed.url": "http://spys.one/en/",
          "feed.provider": "spys.one",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-05-04T11:16:46+00:00"
          }
EVENT1 = {"feed.name": "spys one feed",
          "feed.url": "http://spys.one/en/",
          "feed.provider": "spys.one",
          "time.observation": "2018-05-04T11:16:46+00:00",
          "__type": "Event",
          "classification.type": "proxy",
          "source.ip": "106.104.12.222",
          "time.source": "2018-05-05T10:41:00+00:00",
          "raw": "PHRyIGNsYXNzPSJzcHkxeHgiIG9ubW91c2VvdXQ9InRoaXMuc3R5bGUuYmFja2dyb3VuZD0nIzAwMzM"
                 "zMyciIG9ubW91c2VvdmVyPSJ0aGlzLnN0eWxlLmJhY2tncm91bmQ9JyMwMDI0MjQnIj48dGQgY29sc3"
                 "Bhbj0iMSI+wqA8Zm9udCBjbGFzcz0ic3B5MTQiPjEwNi4xMDQuMTIuMjIyPHNjcmlwdCB0eXBlPSJ0Z"
                 "Xh0L2phdmFzY3JpcHQiPmRvY3VtZW50LndyaXRlKCI8Zm9udCBjbGFzcz1zcHkyPjo8XC9mb250PiIr"
                 "KFNpeFplcm9FaWdodE9uZV5UaHJlZTNUd28pKyhaZXJvNVNldmVuVHdvXlplcm9Ud29OaW5lKSk8L3N"
                 "jcmlwdD48L2ZvbnQ+PC90ZD48dGQgY29sc3Bhbj0iMSI+PGZvbnQgY2xhc3M9InNweTEiPkhUVFA8Zm"
                 "9udCBjbGFzcz0ic3B5MTQiPlM8L2ZvbnQ+PC9mb250PjwvdGQ+PHRkIGNvbHNwYW49IjEiPjxmb250I"
                 "GNsYXNzPSJzcHkyIj5BTk08L2ZvbnQ+PC90ZD48dGQgY29sc3Bhbj0iMSI+PGZvbnQgY2xhc3M9InNw"
                 "eTE0Ij48YWNyb255bSB0aXRsZT0iVGFpd2FuIChUVykgVGFpcGVpIj5UYWl3YW48L2Fjcm9ueW0+PC9"
                 "mb250PjwvdGQ+PHRkIGNvbHNwYW49IjEiPjxmb250IGNsYXNzPSJzcHkxIj48YWNyb255bSB0aXRsZT"
                 "0iMTEgb2YgNTIgLSBsYXN0IGNoZWNrIHN0YXR1cz1PSyI+MjElIDxmb250IGNsYXNzPSJzcHkxIj4oM"
                 "TEpPC9mb250PiA8Zm9udCBjbGFzcz0ic3B5NSI+LTwvZm9udD48L2Fjcm9ueW0+PC9mb250PjwvdGQ+"
                 "PHRkIGNvbHNwYW49IjEiPjxmb250IGNsYXNzPSJzcHkxIj4wNS1tYXktMjAxODwvZm9udD48Zm9udCB"
                 "jbGFzcz0ic3B5MTQiPiAxMDo0MTwvZm9udD48L3RkPjwvdHI+"
          }


class TestSpysOneParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = SpysOneParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)


if __name__ == '__main__':
    unittest.main()
