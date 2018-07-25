# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.isc_sans_ip.parser import IscSansIpParserBot
from intelmq.lib import utils


with open(os.path.join(os.path.dirname(__file__), 'test_isc_sans_ip.data'), 'rb') as handle:
    REPORT_DATA = handle.read()

EXAMPLE_REPORT = {"feed.name": "isc-sans-ip",
                  "feed.url": "https://isc.sans.edu/ipsascii.html",
                  "feed.provider": "isc.sans.edu",
                  "__type": "Report",
                  "raw": utils.base64_encode(REPORT_DATA),
                  "time.observation": "2018-07-20T11:19:00+00:00",
                  }

EXAMPLE_EVENT = {"__type": "Event",
                 "feed.name": "isc-sans-ip",
                 "feed.provider": "isc.sans.edu",
                 "feed.url": "https://isc.sans.edu/ipsascii.html",
                 "time.observation": "2018-07-20T11:19:00+00:00",
                 "source.ip": "46.161.27.30",
                 "time.source": "2018-06-01T00:00:00+00:00",
                 "extra.last_seen": "2018-07-18",
                 "classification.type": "blacklist",
                 "raw": "MDQ2LjE2MS4wMjcuMDMwCTkxODQ3MwkxMDIzMgkyMDE4LTA2LTAxCTIwMTgtMDctMTg="
                 }


class TestIscSansIpParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for IscSansIpParserBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = IscSansIpParserBot
        self.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
