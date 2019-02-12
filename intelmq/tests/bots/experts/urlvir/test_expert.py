# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.urlvir.expert import URLvirExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "feed.url": "http://www.urlvir.com/export-hosts/",
                 "time.source": "2018-12-31T18:30:00+00:00",
                 "source.ip": "92.63.197.143"}
EXAMPLE_OUTPUT = {"__type": "Event",
                  'feed.url': 'http://www.urlvir.com/export-hosts/',
                  "source.ip": "92.63.197.143",
                  "malware.hash.md5": "b439982f30b5b47fde89ff1384b671e0",
                  'source.url': 'http://92.63.197.143/systembc/ss.exe',
                  'time.source': '2018-12-31T18:30:00+00:00'}


class TestURLvirExpertBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = URLvirExpertBot

    def test_event(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':
    unittest.main
