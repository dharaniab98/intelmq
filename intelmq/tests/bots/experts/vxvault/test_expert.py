# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.vxvault.expert import VXVaultExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "feed.url": "http://vxvault.net/ViriList.php",
                 "time.observation": "2019-01-19T09:18:44+00:00",
                 "source.url": "http://laflamme-heli.com/wp-includes/ID3/ssj.jpg",
                 "source.ip": "109.234.162.26",
                 "malware.hash.md5": "8A714AD99AE5DBD5FD8432EFAFB5B8E6",
                 "extra.vxvault_link": "http://vxvault.net/ViriFiche.php?ID=39911",
                 "classification.type": "malware"
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "feed.url": "http://vxvault.net/ViriList.php",
                  "time.observation": "2019-01-19T09:18:44+00:00",
                  "source.url": "http://laflamme-heli.com/wp-includes/ID3/ssj.jpg",
                  "source.ip": "109.234.162.26",
                  "malware.hash.md5": "8A714AD99AE5DBD5FD8432EFAFB5B8E6",
                  "extra.vxvault_link": "http://vxvault.net/ViriFiche.php?ID=39911",
                  "classification.type": "malware",
                  "malware.hash.sha1": "D8418DF846E93DA657312ACD64A671887E8D0FA7",
                  "malware.hash.sha256": "E43FB62C12FCF1BE9F9982E81A59350A8F9DD2389198C0B332CEF832A63AAC0F",
                  "time.source": "2019-01-18T00:00:00+00:00"
                  }


class TestVXVaultExpertBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = VXVaultExpertBot

    def test_event(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':
    unittest.main
