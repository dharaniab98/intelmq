# -*- coding: utf-8 -*-
"""
Testing AbusechURLhausAPIExpertBot.
"""

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.abusech.expert_urlhaus import AbusechURLhausAPIExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "feed.name": "Abusech URLhaus Feed",
                 "time.observation": "2019-07-26T16:51:07+00:00",
                 "source.url": "http://dobresmaki.eu/wp-content/plugins/duplicate-post/art.exe"
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "feed.name": "Abusech URLhaus Feed",
                  "time.observation": "2019-07-26T16:51:07+00:00",
                  "source.url": "http://dobresmaki.eu/wp-content/plugins/duplicate-post/art.exe",
                  "extra.VT_link": "https://www.virustotal.com/file/d0357625c0092bc600bdeba2e15"
                                   "62ff6b6618326d7e787e4e738bbc8d9df8af4/analysis/1564090992/",
                  "extra.VT_status": "18 / 68",
                  "extra.file_type": "exe",
                  "malware.hash.md5": "0a7512354df492e21056b43cea193476",
                  "malware.hash.sha256": "d0357625c0092bc600bdeba2e1562ff6b6618326d7e787e4e738bbc8d9df8af4"
                  }


class TestAbusechURLhausAPIExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusechURLhausAPIExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AbusechURLhausAPIExpertBot

    def test_event(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':
    unittest.main
