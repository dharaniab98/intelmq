# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.talos.expert import TalosExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "feed.name": "Talos Feed",
                 "feed.provider": "talosintelligence.com",
                 "feed.url": "https://www.talosintelligence.com/sb_api/query_lookup?query=%2Fapi"
                             "%2Fv2%2Ftop_stats%2Ftop_senders&query_entry%5Bduration%5D=lastday&"
                             "query_entry%5Blimit%5D=100&query_entry%5Bsender_type%5D=virus",
                 "source.fqdn": "cea2.serveur-dedie.fr",
                 "source.ip": "91.212.205.208",
                 "classification.type": "malware",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "feed.name": "Talos Feed",
                  "feed.provider": "talosintelligence.com",
                  "feed.url": "https://www.talosintelligence.com/sb_api/query_lookup?query=%2Fapi"
                              "%2Fv2%2Ftop_stats%2Ftop_senders&query_entry%5Bduration%5D=lastday&"
                              "query_entry%5Blimit%5D=100&query_entry%5Bsender_type%5D=virus",
                  "source.fqdn": "cea2.serveur-dedie.fr",
                  "source.ip": "91.212.205.208",
                  "classification.type": "malware",
                  "extra.tag": "spam"
                  }


class TestTalosExpertBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TalosExpertBot

    def test_event(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':
    unittest.main
