# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.malshare_api.parser import MalshareAPIParserBot

with open(os.path.join(os.path.dirname(__file__), 'test_malshare.data'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

OUTPUT1 = {'__type': 'Event',
           'classification.type': 'malware',
           'malware.hash.md5': '81a6b5e65e1cc4340d7fd60ec30997b8',
           'malware.hash.sha1': '8694f71cbf677098d36cd158f846457dff8de3b4',
           'malware.hash.sha256': '2d825f92a8cc4e906169757d9b9a87d19bd92e2d517fb0c79d726c63d01ec35a',
           'raw': 'eyJtZDUiOiAiODFhNmI1ZTY1ZTFjYzQzNDBkN2ZkNjBlYzMwOTk3YjgiLCAic2hhMSI6ICI4Njk0Zjcx'
                  'Y2JmNjc3MDk4ZDM2Y2QxNThmODQ2NDU3ZGZmOGRlM2I0IiwgInNoYTI1NiI6ICIyZDgyNWY5MmE4Y2M0'
                  'ZTkwNjE2OTc1N2Q5YjlhODdkMTliZDkyZTJkNTE3ZmIwYzc5ZDcyNmM2M2QwMWVjMzVhIn0='}


class TestMalshareAPIParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for MalshareAPIParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = MalshareAPIParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
