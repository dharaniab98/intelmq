# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.apnic_rdap.expert import APNICExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "119.155.153.14",
                 "time.observation": "2019-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "119.155.153.14",
                  "extra.abuse": ["abuse.irt@ptcl.net", "csirt@ptcl.net"],
                  "extra.email": ["munir.ahmed@ptcl.net.pk"],
                  "time.observation": "2019-01-01T00:00:00+00:00",
                  }
EXAMPLE_INPUT6 = {"__type": "Event",
                  "destination.ip": "2001:500:88:200::8",
                  "time.observation": "2019-01-01T00:00:00+00:00",
                  }
EXAMPLE_OUTPUT6 = {"__type": "Event",
                   "destination.ip": "2001:500:88:200::8",
                   "extra.email": ["terry.manderson@icann.org",
                                   "darren.kara@icann.org",
                                   "josh.jenkins@icann.org",
                                   "david.soltero@icann.org",
                                   "david.closson@icann.org",
                                   "ops@icann.org"],
                   "time.observation": "2019-01-01T00:00:00+00:00",
                   }
EXAMPLE_NETWORK_INPUT = {"__type": "Event",
                         "source.network": "119.152.0.0/13",
                         "time.observation": "2019-01-01T00:00:00+00:00",
                         }
EXAMPLE_NETWORK_OUTPUT = {"__type": "Event",
                          "source.network": "119.152.0.0/13",
                          "extra.abuse": ["abuse.irt@ptcl.net", "csirt@ptcl.net"],
                          "extra.email": ["munir.ahmed@ptcl.net.pk"],
                          "time.observation": "2019-01-01T00:00:00+00:00",
                          }
EMPTY_INPUT = {"__type": "Event",
               "source.ip": "127.0.0.1",  # no result
               "time.observation": "2019-01-01T00:00:00+00:00",
               }


class TestAPNICExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for APNICExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = APNICExpertBot
        cls.use_cache = True
        cls.sysconfig = {"pool_size": 10}

    def test_ipv4_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_ipv6_lookup(self):
        self.input_message = EXAMPLE_INPUT6
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT6)

    def test_network_lookup(self):
        self.input_message = EXAMPLE_NETWORK_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_NETWORK_OUTPUT)

    def test_empty_result(self):
        self.input_message = EMPTY_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EMPTY_INPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
