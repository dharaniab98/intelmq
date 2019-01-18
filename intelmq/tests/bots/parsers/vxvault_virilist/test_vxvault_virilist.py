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
          "source.url": "http://awas.ws/Fzz7/",
          "time.observation": "2018-05-04T11:16:46+00:00",
          "time.source": "2018-05-09T00:00:00+00:00",
          "__type": "Event",
          "extra.vxvault_link": "http://vxvault.net/ViriFiche.php?ID=38159",
          "malware.hash.md5": "908ED7911DB05BA330DFA54A031D5694",
          "classification.type": "malware",
          "source.ip": "185.41.186.236",
          "malware.hash.sha1": "FEF7BAD2F4B12A37072E0F692C58E760EAF8A88F",
          "malware.hash.sha256": "E6C45CAB54F8D76453B6A391DCD91456904F5C3711A70EBFB21331CEEB8A1632",
          "raw": "PGRpdiBpZD0icGFnZSI+CjxoMz48aW1nIHNyYz0iVmlydXMucG5nIiBzdHlsZT0idmVydGljYWwtYWxpZ246bWlkZGxl"
                 "Ii8+IE1hbHdhcmUuV2luMzIuU2FtcGxlPC9oMz4KPGJyLz4KPGI+RmlsZTo8L2I+IHNhbXBsZTxici8+CjxiPlNpemU6"
                 "PC9iPiAyNTgwNDg8YnIvPgo8Yj5NRDU6PC9iPiA5MDhFRDc5MTFEQjA1QkEzMzBERkE1NEEwMzFENTY5NDxici8+Cjxi"
                 "PlNIQS0xOjwvYj4gRkVGN0JBRDJGNEIxMkEzNzA3MkUwRjY5MkM1OEU3NjBFQUY4QTg4Rjxici8+CjxiPlNIQS0yNTY6"
                 "PC9iPiBFNkM0NUNBQjU0RjhENzY0NTNCNkEzOTFEQ0Q5MTQ1NjkwNEY1QzM3MTFBNzBFQkZCMjEzMzFDRUVCOEExNjMy"
                 "PGJyLz4KPGI+TGluazo8L2I+IGh4eHA6Ly9hd2FzLndzL0Z6ejcvPGJyLz4KPGI+SVA6PC9iPiAxODUuNDEuMTg2LjIz"
                 "Njxici8+CjxiPkFkZGVkOjwvYj4gMjAxOC0wNS0wOTxici8+CjxiPlRvb2xzOjwvYj4gPGEgaHJlZj0iaHR0cDovL3Bl"
                 "ZHVtcC5tZS85MDhlZDc5MTFkYjA1YmEzMzBkZmE1NGEwMzFkNTY5NCI+W1BFRHVtcF08L2E+IDxhIGhyZWY9Imh0dHBz"
                 "Oi8vd3d3LnZpcnVzdG90YWwuY29tL2ZyL2ZpbGUvZTZjNDVjYWI1NGY4ZDc2NDUzYjZhMzkxZGNkOTE0NTY5MDRmNWMz"
                 "NzExYTcwZWJmYjIxMzMxY2VlYjhhMTYzMi9hbmFseXNpcy8iPltWaXJ1c1RvdGFsXTwvYT4gPGEgaHJlZj0iaHR0cDov"
                 "L3VybHF1ZXJ5Lm5ldC9zZWFyY2g/cT0xODUuNDEuMTg2LjIzNiI+W1VybFF1ZXJ5XTwvYT4gPGEgaHJlZj0iaHR0cHM6"
                 "Ly90b3RhbGhhc2guY3ltcnUuY29tL3NlYXJjaC8/aXA6MTg1LjQxLjE4Ni4yMzYiPltUb3RhbEhhc2hdPC9hPiA8YSBo"
                 "cmVmPSJodHRwOi8vc2VjdWJveGxhYnMuZnIva29sYWIvYXBpP2hhc2g9RkVGN0JBRDJGNEIxMkEzNzA3MkUwRjY5MkM1"
                 "OEU3NjBFQUY4QTg4RiZhbXA7a2V5PTkiPltTZWN1Ym94TGFic108L2E+CjxhIGhyZWY9Imh0dHBzOi8vd3d3Lmh5YnJp"
                 "ZC1hbmFseXNpcy5jb20vc2VhcmNoP3F1ZXJ5PWU2YzQ1Y2FiNTRmOGQ3NjQ1M2I2YTM5MWRjZDkxNDU2OTA0ZjVjMzcx"
                 "MWE3MGViZmIyMTMzMWNlZWI4YTE2MzIiPltIeWJyaWRdPC9hPgo8YnIvPgo8YnIvPjxoMz48YSBocmVmPSJmaWxlcy85"
                 "MDhFRDc5MTFEQjA1QkEzMzBERkE1NEEwMzFENTY5NC56aXAiPjxpbWcgYm9yZGVyPSIwIiBzcmM9IlBhY2thZ2UucG5n"
                 "IiBzdHlsZT0idmVydGljYWwtYWxpZ246bWlkZGxlIi8+IERvd25sb2FkIEZpbGU8L2E+PC9oMz4KPGJyLz48YnIvPgo8L2Rpdj4="
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
