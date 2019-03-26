# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.guardicore.parser import GuardicoreParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_attackers.data')) as handle:
    REPORT_DATA1 = handle.read()
with open(os.path.join(os.path.dirname(__file__), 'test_malicious_domains.data')) as handle:
    REPORT_DATA2 = handle.read()
with open(os.path.join(os.path.dirname(__file__), 'test_malicious_cc.data')) as handle:
    REPORT_DATA3 = handle.read()
with open(os.path.join(os.path.dirname(__file__), 'test_scanners.data')) as handle:
    REPORT_DATA4 = handle.read()

REPORT1 = {"__type": "Report",
           "feed.name": "Guardicore Top Attackers IP Feed",
           "feed.url": "https://threatintelligence.guardicore.com/code/data/top_attackers.js",
           "feed.provider": "guardicore.com",
           "raw": utils.base64_encode(REPORT_DATA1),
           "time.observation": "2019-03-26T00:00:00+00:00"
           }
REPORT2 = {"__type": "Report",
           "feed.name": "Guardicore Malicious Domains Feed",
           "feed.url": "https://threatintelligence.guardicore.com/code/data/malicious_domains.js",
           "feed.provider": "guardicore.com",
           "raw": utils.base64_encode(REPORT_DATA2),
           "time.observation": "2019-03-26T00:00:00+00:00"
           }
REPORT3 = {"__type": "Report",
           "feed.name": "Guardicore Botnet IP Feed",
           "feed.url": "https://threatintelligence.guardicore.com/code/data/malicious_cc.js",
           "feed.provider": "guardicore.com",
           "raw": utils.base64_encode(REPORT_DATA3),
           "time.observation": "2019-03-26T00:00:00+00:00"
           }
REPORT4 = {"__type": "Report",
           "feed.name": "Guardicore Scanner IP Feed",
           "feed.url": "https://threatintelligence.guardicore.com/code/data/top_scanners.js",
           "feed.provider": "guardicore.com",
           "raw": utils.base64_encode(REPORT_DATA4),
           "time.observation": "2019-03-26T00:00:00+00:00"
           }


EVENT1 = {"feed.name": "Guardicore Top Attackers IP Feed",
          "feed.url": "https://threatintelligence.guardicore.com/code/data/top_attackers.js",
          "feed.provider": "guardicore.com",
          "time.observation": "2019-03-26T00:00:00+00:00",
          "__type": "Event",
          "classification.type": "malware",
          "source.ip": "157.230.189.193",
          "raw": "MTU3LjIzMC4xODkuMTkz"
          }

EVENT2 = {"feed.name": "Guardicore Malicious Domains Feed",
          "feed.url": "https://threatintelligence.guardicore.com/code/data/malicious_domains.js",
          "feed.provider": "guardicore.com",
          "time.observation": "2019-03-26T00:00:00+00:00",
          "__type": "Event",
          "classification.type": "malware",
          "source.fqdn": "ip-54-37-70.eu",
          "raw": "aXAtNTQtMzctNzAuZXU="
          }

EVENT3 = {"feed.name": "Guardicore Botnet IP Feed",
          "feed.url": "https://threatintelligence.guardicore.com/code/data/malicious_cc.js",
          "feed.provider": "guardicore.com",
          "time.observation": "2019-03-26T00:00:00+00:00",
          "__type": "Event",
          "classification.type": "c&c",
          "source.ip": "60.2.251.85",
          "raw": "NjAuMi4yNTEuODU="
          }

EVENT4 = {"feed.name": "Guardicore Scanner IP Feed",
          "feed.url": "https://threatintelligence.guardicore.com/code/data/top_scanners.js",
          "feed.provider": "guardicore.com",
          "time.observation": "2019-03-26T00:00:00+00:00",
          "__type": "Event",
          "classification.type": "scanner",
          "source.ip": "141.98.81.100",
          "raw": "MTQxLjk4LjgxLjEwMA=="
          }


class TestGuardicoreParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = GuardicoreParserBot

    def test_event_top_attackers(self):
        self.input_message = REPORT1
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)

    def test_event_malicious_domains(self):
        self.input_message = REPORT2
        self.run_bot()
        self.assertMessageEqual(0, EVENT2)

    def test_event_malicious_cc(self):
        self.input_message = REPORT3
        self.run_bot()
        self.assertMessageEqual(0, EVENT3)

    def test_event_scanners(self):
        self.input_message = REPORT4
        self.run_bot()
        self.assertMessageEqual(0, EVENT4)


if __name__ == '__main__':
    unittest.main
