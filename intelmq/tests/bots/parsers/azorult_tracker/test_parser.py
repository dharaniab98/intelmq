# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.azorult_tracker.parser import AZORultTrackerParserBot

with open(os.path.join(os.path.dirname(__file__), 'test_azorult_tracker.data'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

OUTPUT1 = {'__type': 'Event',
           'source.asn': 198610,
           'source.fqdn': 'dfghr.beget.tech',
           'source.ip': '5.101.153.87',
           'source.url': 'http://dfghr.beget.tech/index.php',
           'status': 'online',
           'time.source': '2020-05-18T16:26:08+00:00',
           'classification.type': 'c&c',
           'raw': 'eyJfaWQiOiAiNWVjMmI3MjBmODc1NzIxNDdiNDQ1NjEyIiwgImlwIjogIjUuMTAxLjE1My44NyIsICJh'
                  'c19vcmciOiAiQmVnZXQgTExDIiwgImFzbiI6ICJBUzE5ODYxMCIsICJjb3VudHJ5X2NvZGUiOiAiUlUi'
                  'LCAicGFuZWxfaW5kZXgiOiAiaHR0cDovL2RmZ2hyLmJlZ2V0LnRlY2gvaW5kZXgucGhwIiwgInBhbmVs'
                  'X3BhdGgiOiAiL3BhbmVsLyIsICJwYW5lbF92ZXJzaW9uIjogIjMuMiIsICJzdGF0dXMiOiAib25saW5l'
                  'IiwgImZlZWRlciI6ICJtYW51YWwiLCAiZmlyc3Rfc2VlbiI6IDE1ODk4MTkxNjgsICJkYXRhIjogeyJk'
                  'YXRlIjogMTU4OTg2MjQ0MiwgImhhY2tlZCI6IGZhbHNlLCAiYm90X3RvdGFsIjogMCwgInBhc3N3b3Jk'
                  'X3RvdGFsIjogMCwgImJvdCI6IHsiYWxsIjogMCwgInRvZGF5IjogMCwgIndlZWsiOiAwLCAibW9udGgi'
                  'OiAwfSwgInBhc3N3b3JkIjoge30sICJjb3VudHJ5Ijoge30sICJhcmNoIjoge30sICJvcyI6IHt9LCAi'
                  'cmlnaHQiOiB7fSwgImJpbmFyeSI6IHt9LCAic29mdHdhcmUiOiB7fSwgImNvbmZpZyI6IHsiaXNEb3Vi'
                  'bGUiOiB0cnVlLCAiaXNTYXZlZFBhc3N3b3JkcyI6IHRydWUsICJpc0Jyb3dzZXJEYXRhIjogdHJ1ZSwg'
                  'ImlzQnJvd3Nlckhpc3RvcnkiOiB0cnVlLCAiaXNXYWxsZXRzIjogdHJ1ZSwgImlzU2t5cGUiOiB0cnVl'
                  'LCAiaXNUZWxlZ3JhbSI6IHRydWUsICJpc1N0ZWFtIjogdHJ1ZSwgImlzU2NyZWVuc2hvdCI6IHRydWUs'
                  'ICJpc0RlbGV0ZSI6IGZhbHNlLCAiZmlsZXMiOiB7IjAiOiB7ImZnTmFtZSI6ICJEZXNrdG9wIiwgImZn'
                  'UGF0aCI6ICIlVVNFUlBST0ZJTEUlL0Rlc2t0b3AiLCAiZmdNYXNrIjogIip0eHQiLCAiZmdNYXhzaXpl'
                  'IjogMTUsICJmZ1N1YmZvbGRlcnMiOiB0cnVlLCAiZmdTaG9ydGN1dHMiOiB0cnVlLCAiZmdFeGNlcHRp'
                  'b25zIjogIiJ9fSwgImxvYWRlciI6IHt9fSwgImltcG9ydGFudF9saW5rcyI6ICIlbWFpbCUifSwgImRv'
                  'bWFpbiI6ICJkZmdoci5iZWdldC50ZWNoIiwgInRsZCI6ICJ0ZWNoIn0='}

class TestAZORultTrackerParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AZORultTrackerParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AZORultTrackerParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
