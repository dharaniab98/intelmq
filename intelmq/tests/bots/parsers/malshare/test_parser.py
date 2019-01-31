# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.malshare.parser import MalshareParserBot

with open(os.path.join(os.path.dirname(__file__), 'test_malshare.data'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

OUTPUT1 = {'__type': 'Event',
           'classification.type': 'malware',
           'extra.file_type': 'gzip',
           'malware.hash.md5': '628933d238a8747c1d0121bb6c408cef',
           'raw': 'PHRyPgo8dGQgY2xhc3M9Imhhc2hfZm9udCI+PGEgaHJlZj0ic2FtcGxlLnBocD9hY3Rpb249ZGV0YWlsJmFtcDtoY'
                  'XNoPTYyODkzM2QyMzhhODc0N2MxZDAxMjFiYjZjNDA4Y2VmIj42Mjg5MzNkMjM4YTg3NDdjMWQwMTIxYmI2YzQwOG'
                  'NlZjwvYT48L3RkPgo8dGQ+Z3ppcDwvdGQ+Cjx0ZD4yMDE5LTAxLTI4IDEyOjI4OjI3IFVUQzwvdGQ+PHRkPmh0dHA'
                  '6Ly93d3cueXh1d3hwcWp0ZG1qLnR3L3F1bmh4YS8xMDU2N185NDgwNC4uLjwvdGQ+IDx0ZD48L3RkPjwvdHI+',
                  'time.source': '2019-01-28T12:28:27+00:00'}

OUTPUT2 = {'__type': 'Event',
           'classification.type': 'malware',
           'extra.file_type': 'gzip',
           'malware.hash.md5': 'f89d0417c669c41bf9ac345ca5ee3d6b',
           'raw': 'PHRyPgo8dGQgY2xhc3M9Imhhc2hfZm9udCI+PGEgaHJlZj0ic2FtcGxlLnBocD9hY3Rpb249ZGV0YWlsJmFtcDtoYXNoPWY4OWQwNDE3YzY'
                  '2OWM0MWJmOWFjMzQ1Y2E1ZWUzZDZiIj5mODlkMDQxN2M2NjljNDFiZjlhYzM0NWNhNWVlM2Q2YjwvYT48L3RkPgo8dGQ+Z3ppcDwvdGQ+Cj'
                  'x0ZD4yMDE5LTAxLTI4IDEyOjIzOjU3IFVUQzwvdGQ+PHRkPmh0dHA6Ly93d3cueHB1bnlzZW94eWdzLnR3L201ak1MQS9ubXdxb2ZueW9nb'
                  'C4uLjwvdGQ+IDx0ZD48L3RkPjwvdHI+',
           'time.source': '2019-01-28T12:23:57+00:00'}


class TestMalshareParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for MalwareDomainsParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = MalshareParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)
        self.assertMessageEqual(1, OUTPUT2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
