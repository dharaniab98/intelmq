# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.guardicore.expert import GuardicoreExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "feed.name": "Guardicore C2 IP Feed",
                 "feed.provider": "guardicore.com",
                 "feed.url": "https://threatintelligence.guardicore.com/code/data/malicious_cc.js",
                 "time.observation": "2019-04-07T12:23:50+00:00",
                 "classification.type": "c&c",
                 "source.ip": "60.2.251.85"}
EXAMPLE_OUTPUT = {"__type": "Event",
                  "feed.name": "Guardicore C2 IP Feed",
                  "feed.provider": "guardicore.com",
                  "feed.url": "https://threatintelligence.guardicore.com/code/data/malicious_cc.js",
                  "time.observation": "2019-04-07T12:23:50+00:00",
                  "classification.type": "c&c",
                  "source.ip": "60.2.251.85",
                  "extra.tags": ["Attacker", "DNS Query", "Create MsSql Procedure", "Drop MsSql Table",
                                 "Outgoing Connection", "Brute Force", "Successful Login",
                                 "MSSQL Brute Force", "Access Suspicious Domain", "Malicious File",
                                 "Successful MSSQL Login", "IDS - Attempted User Privilege Gain",
                                 "Persistency - Logon", "Execute MsSql Shell Command"],
                  "source.fqdn": "js.1226bye.pw"}


class TestGuardicoreExpertBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = GuardicoreExpertBot

    def test_event(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':
    unittest.main
