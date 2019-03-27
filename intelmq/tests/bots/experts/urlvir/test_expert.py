# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.urlvir.expert import URLvirExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "feed.url": "http://www.urlvir.com/export-hosts/",
                 "time.source": "2018-12-31T18:30:00+00:00",
                 "source.fqdn": "puertascuesta.com",
                 "event_description.url": "http://www.urlvir.com/search-host/puertascuesta.com/"
                 }
EXAMPLE_INPUT1 = {"__type": "Event",
                  "feed.url": "http://www.urlvir.com/export-hosts/",
                  "time.source": "2018-12-31T18:30:00+00:00",
                  "source.ip": "134.209.117.229",
                  "event_description.url": "http://www.urlvir.com/search-ip-address/134.209.117.229/"
                  }
EXAMPLE_INPUT2 = {"__type": "Event",
                  "feed.url": "http://www.urlvir.com/export-hosts/",
                  "time.source": "2018-12-31T18:30:00+00:00",
                  "source.fqdn": "akpeugono.com",
                  "event_description.url": "http://www.urlvir.com/search-host/akpeugono.com/"
                  }
EXAMPLE_INPUT3 = {"__type": "Event",
                  "feed.url": "http://www.urlvir.com/export-hosts/",
                  "time.source": "2018-12-31T18:30:00+00:00",
                  "source.ip": "92.63.197.143",
                  "event_description.url": "http://www.urlvir.com/search-ip-address/92.63.197.143/"
                  }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "feed.url": "http://www.urlvir.com/export-hosts/",
                  "malware.hash.md5": "ee21903d559f97bf69d20485fe957735",
                  "source.fqdn": "puertascuesta.com",
                  "source.ip": "185.18.196.224",
                  "source.url": "http://puertascuesta.com/nN5xhDQABfx/",
                  "status": "Active",
                  "time.source": "2019-02-05T18:30:00+00:00",
                  "event_description.url": "http://www.urlvir.com/search-host/puertascuesta.com/"
                  }
EXAMPLE_OUTPUT1 = {"__type": "Event",
                   "feed.url": "http://www.urlvir.com/export-hosts/",
                   "malware.hash.md5": "84a944b2eb27d60264697a641898281f",
                   "source.url": "http://134.209.117.229/bins/air.arm",
                   "status": "Active",
                   "time.source": "2019-03-18T18:30:00+00:00",
                   "source.ip": "134.209.117.229",
                   "event_description.url": "http://www.urlvir.com/search-ip-address/134.209.117.229/"
                   }
EXAMPLE_OUTPUT2 = {"__type": "Event",
                   "feed.url": "http://www.urlvir.com/export-hosts/",
                   "malware.hash.md5": "d8481959affa32e6863954dc07e2e118",
                   "source.ip": "67.220.184.146",
                   "source.url": "http://www.akpeugono.com/joomla30/6kqxd-xk24dk-kcor.view/",
                   "status": "Active",
                   "time.source": "2019-03-08T18:30:00+00:00",
                   "source.fqdn": "akpeugono.com",
                   "event_description.url": "http://www.urlvir.com/search-host/akpeugono.com/"
                   }
EXAMPLE_OUTPUT3 = {"__type": "Event",
                   "feed.url": "http://www.urlvir.com/export-hosts/",
                   "status": "Inactive",
                   "time.source": "2018-12-31T18:30:00+00:00",
                   "source.ip": "92.63.197.143",
                   "event_description.url": "http://www.urlvir.com/search-ip-address/92.63.197.143/"
                   }


class TestURLvirExpertBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = URLvirExpertBot

    def test_event(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_event_replace_ip(self):
        self.input_message = EXAMPLE_INPUT1
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT1)

    def test_event_add_www(self):
        self.input_message = EXAMPLE_INPUT2
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT2)

    def test_event_status_inactive(self):
        self.input_message = EXAMPLE_INPUT3
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT3)


if __name__ == "__main__":
    unittest.main
