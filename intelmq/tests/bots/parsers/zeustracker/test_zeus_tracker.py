# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.zeustracker.parser import ZeusTrackerParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_zeus_tracker.data')) as handle:
    REPORT_DATA = handle.read()

REPORT = {"__type": "Report",
          "feed.name": "Zeus Tracker Feed",
          "feed.url": "https://zeustracker.abuse.ch/monitor.php?filter=all",
          "feed.provider": "abuse.ch",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-12-28T10:31:40+00:00"
          }

EVENT1 = {"feed.name": "Zeus Tracker Feed",
          "feed.url": "https://zeustracker.abuse.ch/monitor.php?filter=all",
          "feed.provider": "abuse.ch",
          "time.observation": "2018-12-28T10:31:40+00:00",
          "time.source": "2018-12-18T00:00:00+00:00",
          "__type": "Event",
          "malware.name": "citadel",
          "classification.type": "c&c",
          "source.ip": "176.107.191.119",
          "raw": "PHRyIGJnY29sb3I9IiNkOGQ4ZDgiPjx0ZD4yMDE4LTEyLTE4PC90ZD48dGQ+Q2l0YWRlbD"
                 "wvdGQ+PHRkPjxhIGhyZWY9Ii9tb25pdG9yLnBocD9ob3N0PTE3Ni4xMDcuMTkxLjExOSIg"
                 "dGFyZ2V0PSJfcGFyZW50IiB0aXRsZT0iR2V0IG1vcmUgaW5mb3JtYXRpb24gYWJvdXQgdG"
                 "hpcyBIb3N0Ij4xNzYuMTA3LjE5MS4xMTk8L2E+PC90ZD48dGQ+PGEgaHJlZj0iL21vbml0"
                 "b3IucGhwP2lwYWRkcmVzcz0xNzYuMTA3LjE5MS4xMTkiIHRhcmdldD0iX3BhcmVudCIgdG"
                 "l0bGU9IkdldCBhIGxpc3Qgb2YgYWxsIFpldVMgQyZhbXA7Q3MgaG9zdGVkIG9uIDE3Ni4x"
                 "MDcuMTkxLjExOSI+MTc2LjEwNy4xOTEuMTE5PC9hPjwvdGQ+PHRkIGJnY29sb3I9IiNDQ0"
                 "NDQ0MiPjQ8L3RkPjx0ZCBiZ2NvbG9yPSIjZDhkOGQ4Ij51bmtub3duPC90ZD48dGQgYWxp"
                 "Z249ImNlbnRlciIgYmdjb2xvcj0iIzAwRkYwMCI+MDwvdGQ+PHRkIGJnY29sb3I9IiMwME"
                 "ZGMDAiPk5vdCBsaXN0ZWQ8L3RkPjx0ZCBhbGlnbj0iY2VudGVyIj48aW1nIGFsdD0iLSIg"
                 "aGVpZ2h0PSIxNCIgc3JjPSJpbWFnZXMvZmxhZ3MvVUEuUE5HIiB0aXRsZT0iVWtyYWluZS"
                 "AoVUEpIiB3aWR0aD0iMTQiLz48L3RkPjx0ZD48YSBocmVmPSIvbW9uaXRvci5waHA/YXM9"
                 "NDIzMzEiIHRhcmdldD0iX3BhcmVudCIgdGl0bGU9IkdldCBhIGxpc3Qgb2YgYWxsIFpldV"
                 "MgQyZhbXA7Q3MgbG9jYXRlZCBpbiBBUzQyMzMxIEZSRUVIT1NUIFBFIEZyZWVob3N0Ij5B"
                 "UzQyMzMxPC9hPjwvdGQ+PHRkIGJnY29sb3I9IiNkOGQ4ZDgiPjxjZW50ZXI+LTwvY2VudG"
                 "VyPjwvdGQ+PC90cj4="
          }
EVENT2 = {"feed.name": "Zeus Tracker Feed",
          "feed.url": "https://zeustracker.abuse.ch/monitor.php?filter=all",
          "feed.provider": "abuse.ch",
          "time.observation": "2018-12-28T10:31:40+00:00",
          "time.source": "2018-11-07T00:00:00+00:00",
          "__type": "Event",
          "malware.name": "citadel",
          "classification.type": "c&c",
          "source.ip": "82.221.113.145",
          "source.fqdn": "brightqain.com",
          "extra.sbl": "SBL423484",
          "extra.status": "online",
          "raw": "PHRyIGJnY29sb3I9IiNkOGQ4ZDgiPjx0ZD4yMDE4LTExLTA3PC90ZD48dGQ+Q2l0YWRlbD"
                 "wvdGQ+PHRkPjxhIGhyZWY9Ii9tb25pdG9yLnBocD9ob3N0PWJyaWdodHFhaW4uY29tIiB0"
                 "YXJnZXQ9Il9wYXJlbnQiIHRpdGxlPSJHZXQgbW9yZSBpbmZvcm1hdGlvbiBhYm91dCB0aG"
                 "lzIEhvc3QiPmJyaWdodHFhaW4uY29tPC9hPjwvdGQ+PHRkPjxhIGhyZWY9Ii9tb25pdG9y"
                 "LnBocD9pcGFkZHJlc3M9ODIuMjIxLjExMy4xNDUiIHRhcmdldD0iX3BhcmVudCIgdGl0bG"
                 "U9IkdldCBhIGxpc3Qgb2YgYWxsIFpldVMgQyZhbXA7Q3MgaG9zdGVkIG9uIDgyLjIyMS4x"
                 "MTMuMTQ1Ij44Mi4yMjEuMTEzLjE0NTwvYT48L3RkPjx0ZCBiZ2NvbG9yPSIjQ0NDQ0NDIj"
                 "40PC90ZD48dGQgYmdjb2xvcj0iI0ZGMDAwMCI+b25saW5lPC90ZD48dGQgYWxpZ249ImNl"
                 "bnRlciIgYmdjb2xvcj0iIzAwRkYwMCI+MDwvdGQ+PHRkIGJnY29sb3I9IiNGRjAwMDAiPj"
                 "xhIGhyZWY9Imh0dHA6Ly93d3cuc3BhbWhhdXMub3JnL3NibC9zYmwubGFzc28/cXVlcnk9"
                 "U0JMNDIzNDg0IiB0YXJnZXQ9Il9ibGFuayI+U0JMNDIzNDg0PC9hPjwvdGQ+PHRkIGFsaW"
                 "duPSJjZW50ZXIiPjxpbWcgYWx0PSItIiBoZWlnaHQ9IjE0IiBzcmM9ImltYWdlcy9mbGFn"
                 "cy9JUy5QTkciIHRpdGxlPSJJY2VsYW5kIChJUykiIHdpZHRoPSIxNCIvPjwvdGQ+PHRkPj"
                 "xhIGhyZWY9Ii9tb25pdG9yLnBocD9hcz01MDYxMyIgdGFyZ2V0PSJfcGFyZW50IiB0aXRs"
                 "ZT0iR2V0IGEgbGlzdCBvZiBhbGwgWmV1UyBDJmFtcDtDcyBsb2NhdGVkIGluIEFTNTA2MT"
                 "MgVEhPUkRDLUFTIFRIT1IgRGF0YSBDZW50ZXIgZWhmIj5BUzUwNjEzPC9hPjwvdGQ+PHRk"
                 "IGJnY29sb3I9IiNGRjAwMDAiPjgzODo1OTo1OTwvdGQ+PC90cj4="
          }


class TestZeusTrackerParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ZeusTrackerParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(2, EVENT2)


if __name__ == '__main__':
    unittest.main
