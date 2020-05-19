# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.fumik0.parser import Fumik0ParserBot

with open(os.path.join(os.path.dirname(__file__), 'test_fumik0.data'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

OUTPUT1 = {'__type': 'Event',
           'extra.file_name': 'fattura.exe',
           'extra.file_size': '222720',
           'malware.hash.md5': '9eae0b7cdeee4c07443f80b8bae7e56c',
           'malware.hash.sha1': '9a8e284bba018192052da78f94554779d52515b2',
           'malware.hash.sha256': 'bd27fe96b334c81e8b62bda3121306619ca317dad8a971daf0639cb896953006',
           'raw': 'eyJmaXJzdF9zZWVuIjogIjIwMjAtMDQtMjIgMDg6MTA6MDMiLCAiaGFzaCI6IHsibWQ1IjogIjllYWUwY'
                  'jdjZGVlZTRjMDc0NDNmODBiOGJhZTdlNTZjIiwgInNoYTEiOiAiOWE4ZTI4NGJiYTAxODE5MjA1MmRhNz'
                  'hmOTQ1NTQ3NzlkNTI1MTViMiIsICJzaGEyNTYiOiAiYmQyN2ZlOTZiMzM0YzgxZThiNjJiZGEzMTIxMzA'
                  '2NjE5Y2EzMTdkYWQ4YTk3MWRhZjA2MzljYjg5Njk1MzAwNiJ9LCAiaGFzaF9zZWVuIjogMSwgImlkIjog'
                  'IjVlOWZmYmRiN2EzMjRmMmU3NWI4MWI2OSIsICJzYW1wbGUiOiB7Im5hbWUiOiAiZmF0dHVyYS5leGUiL'
                  'CAic2l6ZSI6ICIyMjI3MjAifSwgInNlcnZlciI6IHsiQVMiOiAiQVM1NjU3NyIsICJjb3VudHJ5IjogIm'
                  'JnIiwgImRvbWFpbiI6ICJnc3RhdC5ibHVlY2hpcHN0YWZmaW5nLmNvbSIsICJpcCI6ICIxODUuNjguOTM'
                  'uNDgiLCAidXJsIjogImdzdGF0LmJsdWVjaGlwc3RhZmZpbmcuY29tL2ZhdHR1cmEuZXhlIn19',
           'source.asn': 56577,
           'source.fqdn': 'gstat.bluechipstaffing.com',
           'source.ip': '185.68.93.48',
           'source.url': 'http://gstat.bluechipstaffing.com/fattura.exe',
           'time.source': '2020-04-22T08:10:03+00:00',
           'classification.type': 'malware'}

class TestFumik0ParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for Fumik0ParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = Fumik0ParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
