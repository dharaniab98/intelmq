# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.vxvault_virilist.parser import VXVaultViriListParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_vxvault_virilist.data')) as handle:
    REPORT_DATA = handle.read()

REPORT = {"__type": "Report",
          "feed.name": "VXVault ViriList Feed",
          "feed.url": "http://vxvault.net/ViriList.php",
          "feed.provider": "vxvault.net",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-05-10T11:16:46+00:00"
          }

EVENT1 = {"feed.name": "VXVault ViriList Feed",
          "feed.url": "http://vxvault.net/ViriList.php",
          "feed.provider": "vxvault.net",
          'source.url': 'http://awas.ws/Fzz7/',
          "time.observation": "2018-05-04T11:16:46+00:00",
          "__type": "Event",
          'malware.hash.md5': '908ED7911DB05BA330DFA54A031D5694',
          "extra.vxvault_link": "http://vxvault.net/ViriFiche.php?ID=38159",
          "classification.type": "malware",
          "source.ip": "185.41.186.236",
          "raw": "PHRyPgo8dGQgY2xhc3M9ImZvbmNlIj48YSBjbGFzcz0icm91Z2UiIGhyZWY9IlZpcmlGaWNoZS5wa"
                 "HA/SUQ9MzgxNTkiPjA1LTA5PC9hPjwvdGQ+Cjx0ZCBjbGFzcz0iZm9uY2UiPjxhIGNsYXNzPSJyb3"
                 "VnZSIgaHJlZj0iZmlsZXMvOTA4RUQ3OTExREIwNUJBMzMwREZBNTRBMDMxRDU2OTQuemlwIj5bRF0"
                 "8L2E+IDxhIGNsYXNzPSJyb3VnZSIgaHJlZj0iVmlyaUZpY2hlLnBocD9JRD0zODE1OSI+YXdhcy53"
                 "cy9Geno3LzwvYT48L3RkPgo8dGQgY2xhc3M9ImZvbmNlIj48YSBjbGFzcz0icm91Z2UiIGhyZWY9I"
                 "lZpcmlMaXN0LnBocD9NRDU9OTA4RUQ3OTExREIwNUJBMzMwREZBNTRBMDMxRDU2OTQiPjkwOEVENz"
                 "kxMURCMDVCQTMzMERGQTU0QTAzMUQ1Njk0PC9hPjwvdGQ+Cjx0ZCBjbGFzcz0iZm9uY2UiPjxhIGN"
                 "sYXNzPSJyb3VnZSIgaHJlZj0iVmlyaUxpc3QucGhwP0lQPTE4NS40MS4xODYuMjM2Ij4xODUuNDEu"
                 "MTg2LjIzNjwvYT7CoDwvdGQ+Cjx0ZCBjbGFzcz0iZm9uY2UiPjxhIGhyZWY9Imh0dHA6Ly9wZWR1b"
                 "XAubWUvOTA4ZWQ3OTExZGIwNWJhMzMwZGZhNTRhMDMxZDU2OTQiPlBFRDwvYT4KPGEgaHJlZj0iaH"
                 "R0cDovL3VybHF1ZXJ5Lm5ldC9zZWFyY2g/cT0xODUuNDEuMTg2LjIzNiI+VVE8L2E+CjwvdGQ+CjwvdHI+"
          }


class TestVXVaultViriListParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = VXVaultViriListParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)


if __name__ == '__main__':
    unittest.main
