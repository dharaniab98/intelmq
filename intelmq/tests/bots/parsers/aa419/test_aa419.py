# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.aa419.parser import Aa419ParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_aa419.data')) as handle:
    REPORT_DATA = handle.read()


REPORT = {"__type": "Report",
          "feed.name": "fake sites list feed",
          "feed.url": "https://db.aa419.org/fakebankslist.php",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-03-03T11:25:09+00:00"
          }
EVENT1 = {"feed.url": "https://db.aa419.org/fakebankslist.php",
          "time.observation": "2018-03-03T11:25:09+00:00",
          "raw": "PHRyIGNsYXNzPSJld1RhYmxlUm93Ij4KPHRkPjxhIGhyZWY9ImZha2ViYW5rc3ZpZXcucGhwP2tleT0xMzAwOTIiPj"
                 "xzcGFuIGNsYXNzPSJwaHBtYWtlciI+PGltZyBhbHQ9IlZpZXciIGJvcmRlcj0iMCIgaGVpZ2h0PSIxNiIgc3JjPSJp"
                 "bWFnZXMvYnJvd3NlLmdpZiIgd2lkdGg9IjE2Ii8+PC9zcGFuPjwvYT48L3RkPgo8dGQ+PGEgaHJlZj0iaHR0cDovL3"
                 "d3dy5jb2FzdGFsb2lsZ2FzY29ycC5jb20iIHJlbD0ibm9mb2xsb3ciIHRhcmdldD0iX2JsYW5rIj5odHRwOi8vd3d3"
                 "LmNvYXN0YWxvaWxnYXNjb3JwLmNvbTwvYT7CoDwvdGQ+Cjx0ZD5Db2FzdGFsIE9pbCAmYW1wOyBHYXMgQ29ycC7CoD"
                 "wvdGQ+Cjx0ZCBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjogcmdiYSgyNTUsMCwwLDAuMTUpOyI+YWN0aXZlwqA8L3Rk"
                 "Pgo8dGQ+MjAxOC0wMy0wMyAwOTo0N8KgPC90ZD4KPHRkPjIwMTgtMDMtMDMgMDk6NDfCoDwvdGQ+CjwvdHI+",
          "feed.name": "fake sites list feed",
          "extra.last_updated": "2018-03-03 09:47",
          "extra.phishing_site": "Coastal Oil & Gas Corp.",
          "extra.phishing_status": "active",
          "source.url": "http://www.coastaloilgascorp.com",
          "classification.type": "phishing",
          "time.source": "2018-03-03T09:47:00+00:00",
          "__type": "Event"}
EVENT2 = {"__type": "Event",
          "feed.name": "fake sites list feed",
          "extra.last_updated": "2018-03-03 08:55",
          "extra.phishing_site": "VP Investment Bank",
          "extra.phishing_status": "active",
          "raw": "PHRyIGNsYXNzPSJld1RhYmxlQWx0Um93Ij4KPHRkPjxhIGhyZWY9ImZha2ViYW5rc3ZpZXcucGhwP2tleT0xMzAwOT"
                 "EiPjxzcGFuIGNsYXNzPSJwaHBtYWtlciI+PGltZyBhbHQ9IlZpZXciIGJvcmRlcj0iMCIgaGVpZ2h0PSIxNiIgc3Jj"
                 "PSJpbWFnZXMvYnJvd3NlLmdpZiIgd2lkdGg9IjE2Ii8+PC9zcGFuPjwvYT48L3RkPgo8dGQ+PGEgaHJlZj0iaHR0cD"
                 "ovL3d3dy52cHJpdmF0ZW9ubGluZS5jb20iIHJlbD0ibm9mb2xsb3ciIHRhcmdldD0iX2JsYW5rIj5odHRwOi8vd3d3"
                 "LnZwcml2YXRlb25saW5lLmNvbTwvYT7CoDwvdGQ+Cjx0ZD5WUCBJbnZlc3RtZW50IEJhbmvCoDwvdGQ+Cjx0ZCBzdH"
                 "lsZT0iYmFja2dyb3VuZC1jb2xvcjogcmdiYSgyNTUsMCwwLDAuMTUpOyI+YWN0aXZlwqA8L3RkPgo8dGQ+MjAxOC0w"
                 "My0wMyAwODo1NcKgPC90ZD4KPHRkPjIwMTgtMDMtMDMgMDg6NTXCoDwvdGQ+CjwvdHI+",
          "time.observation": "2018-03-03T11:25:09+00:00",
          "time.source": "2018-03-03T08:55:00+00:00",
          "classification.type": "phishing",
          "source.url": "http://www.vprivateonline.com",
          "feed.url": "https://db.aa419.org/fakebankslist.php"}


class TestAa419ParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = Aa419ParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)


if __name__ == '__main__':
    unittest.main()
