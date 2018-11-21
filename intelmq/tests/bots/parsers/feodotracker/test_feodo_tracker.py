# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.feodotracker.parser import FeodoTrackerParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_feodo_tracker.data')) as handle:
    REPORT_DATA = handle.read()

REPORT = {"__type": "Report",
          "feed.name": "Feodo Tracker Feed",
          "feed.url": "https://feodotracker.abuse.ch/",
          "feed.provider": "feodotracker.abuse.ch",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-05-10T11:16:46+00:00"
          }

EVENT1 = {"feed.name": "Feodo Tracker Feed",
          "feed.url": "https://feodotracker.abuse.ch/",
          "feed.provider": "feodotracker.abuse.ch",
          "time.observation": "2018-05-04T11:16:46+00:00",
          "time.source": "2018-06-26T05:26:27+00:00",
          "__type": "Event",
          "malware.name": "emotet",
          'status': 'online',
          "classification.type": "c&c",
          "source.ip": "24.121.176.48",
          "raw": "PHRyIGJnY29sb3I9IiM4MzdiN2IiIG9ubW91c2VvdXQ9InRoaXMuc3R5bGUuYmFja2dyb3Vu"
                 "ZENvbG9yPScjODM3YjdiJzsiIG9ubW91c2VvdmVyPSJ0aGlzLnN0eWxlLmJhY2tncm91bmRDb"
                 "2xvcj0nI0ZGQTIwMCc7Ij48dGQ+MjAxOC0wNi0yNiAwNToyNjoyNzwvdGQ+PHRkIGFsaWduPS"
                 "JjZW50ZXIiIGJnY29sb3I9IiNGRjQwMDAiPjxzdHJvbmc+RTwvc3Ryb25nPjwvdGQ+PHRkPjx"
                 "hIGhyZWY9Ii9ob3N0LzI0LjEyMS4xNzYuNDgvIiB0YXJnZXQ9Il9wYXJlbnQiIHRpdGxlPSJT"
                 "aG93IG1vcmUgaW5mb3JtYXRpb24gYWJvdXQgdGhpcyBGZW9kbyBDJmFtcDtDIj4yNC4xMjEuM"
                 "Tc2LjQ4PC9hPjwvdGQ+PHRkIGJnY29sb3I9IiNiYzU5NTkiPm9ubGluZTwvdGQ+PHRkIGJnY2"
                 "9sb3I9IiM0Zjg4M2YiPk5vdCBsaXN0ZWQ8L3RkPjx0ZD5BUzE5MTA4IFNVRERFTkxJTkstQ09"
                 "NTVVOSUNBVElPTlM8L3RkPjx0ZD48aW1nIGFsdD0iLSIgaGVpZ2h0PSIxMCIgc3JjPSJpbWFn"
                 "ZXMvZmxhZ3MvdXMuZ2lmIiB0aXRsZT0iVVMgKFVTKSIgd2lkdGg9IjE2Ii8+IFVTPC90ZD48d"
                 "GQ+bmV2ZXI8L3RkPjwvdHI+"
          }


class TestFeodoTrackerParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FeodoTrackerParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)


if __name__ == '__main__':
    unittest.main
