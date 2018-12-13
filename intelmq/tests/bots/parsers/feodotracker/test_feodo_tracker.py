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
          "feed.url": "https://feodotracker.abuse.ch/browse/",
          "feed.provider": "abuse.ch",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-12-12T09:06:08+00:00"
          }

EVENT1 = {"feed.name": "Feodo Tracker Feed",
          "feed.url": "https://feodotracker.abuse.ch/browse/",
          "feed.provider": "abuse.ch",
          "time.observation": "2018-12-12T09:06:08+00:00",
          "time.source": "2018-12-11T21:33:10+00:00",
          "__type": "Event",
          "malware.name": "heodo",
          "status": "Online",
          "classification.type": "c&c",
          "source.asn": 5769,
          "source.ip": "96.21.235.243",
          "raw": "PHRyPjx0ZD4yMDE4LTEyLTExIDIxOjMzOjEwPC90ZD48dGQ+PGEgaHJlZj0iL"
                 "2Jyb3dzZS9ob3N0Lzk2LjIxLjIzNS4yNDMvIiB0YXJnZXQ9Il9wYXJlbnQiIH"
                 "RpdGxlPSJHZXQgbW9yZSBpbmZvcm1hdGlvbiBhYm91dCB0aGlzIGJvdG5ldCB"
                 "DJmFtcDtDIj45Ni4yMS4yMzUuMjQzPC9hPjwvdGQ+PHRkPjxzcGFuIGNsYXNz"
                 "PSJiYWRnZSBiYWRnZS1pbmZvIj5IZW9kbyA8YSBocmVmPSJodHRwczovL21hb"
                 "HBlZGlhLmNhYWQuZmtpZS5mcmF1bmhvZmVyLmRlL2RldGFpbHMvd2luLmdlb2"
                 "RvIiB0YXJnZXQ9Il9ibGFuayIgdGl0bGU9Ik1hbHBlZGlhOiBHZW9kbyAoYWt"
                 "hIEVtb3RldCBha2EgSGVvZG8pIj48aW1nIGFsdD0iLSIgaGVpZ2h0PSIxMiIg"
                 "c3JjPSIvaW1hZ2VzL2ljb25zL2xpbmstZXh0ZXJuYWwuc3ZnIiB3aWR0aD0iM"
                 "TIiLz48L2E+PC9zcGFuPjwvdGQ+PHRkPjxzcGFuIGNsYXNzPSJiYWRnZSBiYW"
                 "RnZS1kYW5nZXIiPjxpbWcgYWx0PSItIiBzcmM9Ii9pbWFnZXMvaWNvbnMvZmx"
                 "hbWUuc3ZnIi8+ICBPbmxpbmU8L3NwYW4+PC90ZD48dGQ+Tm90IGxpc3RlZDwv"
                 "dGQ+PHRkIGNsYXNzPSJ0ZXh0LXRydW5jYXRlIj5BUzU3NjkgVklERU9UUk9OI"
                 "C0gVmlkZW90cm9uIFRlbGVjb20gTHRlZTwvdGQ+PHRkPjxpbWcgYWx0PSItIi"
                 "BzcmM9ImltYWdlcy9mbGFncy9jYS5wbmciIHRpdGxlPSJDQSIvPiBDQTwvdGQ+PC90cj4="
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
