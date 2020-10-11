# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.json_custom.parser import JSONCustomParserBot

with open(os.path.join(os.path.dirname(__file__), 'data1.json'), 'rb') as fh:
    RAW1 = base64.b64encode(fh.read()).decode()

MULTILINE_REPORT = {"feed.name": "RSTThreats Domain Feed",
                    "raw": RAW1,
                    "__type": "Report",
                    }
MULTILINE_EVENTS = [{'__type': 'Event',
                     'classification.type': 'malware',
                     'extra.tags': ['spam'],
                     'extra.threat_info': [],
                     'feed.name': 'RSTThreats Domain Feed',
                     'raw': 'eyJkb21haW4iOiAiZHJvcGJveC1kb3dubG9hZC5jb20iLCAiZnNlZW4iOiAxNTk0MzM5Mj'
                            'AwLCAibHNlZW4iOiAxNjAxOTQyNDAwLCAiY29sbGVjdCI6IDE2MDIwMjg4MDAsICJ0YWdz'
                            'IjogeyJzdHIiOiBbInNwYW0iXSwgImNvZGVzIjogWzJdfSwgInJlc29sdmVkIjogeyJpcC'
                            'I6IHsiYSI6IFsiMTguMjM1LjkyLjEyMyJdLCAiYWxpYXMiOiBbXSwgImNuYW1lIjogW119'
                            'LCAid2hvaXMiOiB7ImNyZWF0ZWQiOiAiMjAxOS0xMC0wMSAyMDoxOTozNCIsICJ1cGRhdG'
                            'VkIjogIjIwMTktMTAtMjEgMDY6Mjc6MTEiLCAiZXhwaXJlcyI6ICIyMDIwLTEwLTAxIDIw'
                            'OjE5OjM0IiwgImFnZSI6IDM2NSwgInJlZ2lzdHJhciI6ICJQRFIgTHRkIGRiYSBQdWJsaW'
                            'NEb21haW5SZWdpc3RyeWNvbSIsICJyZWdpc3RyYW50IjogInVua25vd24iLCAiaGF2ZWRh'
                            'dGEiOiAidHJ1ZSJ9fSwgInNjb3JlIjogeyJ0b3RhbCI6IDE0LCAic3JjIjogNjAuMiwgIn'
                            'RhZ3MiOiAwLjc1LCAiZnJlcXVlbmN5IjogMC4zMn0sICJmcCI6IHsiYWxhcm0iOiAiZmFs'
                            'c2UiLCAiZGVzY3IiOiAiIn0sICJ0aHJlYXQiOiBbXSwgImlkIjogIjRlYTc4MmE2LTlhZW'
                            'YtM2ViOC04M2U3LTNjMzUxMDc1ZjUzMCIsICJ0aXRsZSI6ICJSU1QgVGhyZWF0IGZlZWQu'
                            'IElPQzogZHJvcGJveC1kb3dubG9hZC5jb20iLCAiZGVzY3JpcHRpb24iOiAiSU9DIHdpdG'
                            'ggdGFnczogc3BhbSJ9',
                     'source.fqdn': 'dropbox-download.com',
                     'source.ip': '18.235.92.123',
                     'time.source': '2020-10-06T00:00:00+00:00'
                     },
                    {'__type': 'Event',
                     'classification.type': 'malware',
                     'extra.tags': ['malware'],
                     'extra.threat_info': [],
                     'feed.name': 'RSTThreats Domain Feed',
                     'raw': 'eyJkb21haW4iOiAiZGNoYW1iYW50b3RhLmNvbSIsICJmc2VlbiI6IDE1OTg0ODY0MDAsIC'
                            'Jsc2VlbiI6IDE2MDE5NDI0MDAsICJjb2xsZWN0IjogMTYwMjAyODgwMCwgInRhZ3MiOiB7'
                            'InN0ciI6IFsibWFsd2FyZSJdLCAiY29kZXMiOiBbMTBdfSwgInJlc29sdmVkIjogeyJpcC'
                            'I6IHsiYSI6IFsiMTExLjIyMS40Ni43NSJdLCAiYWxpYXMiOiBbXSwgImNuYW1lIjogW119'
                            'LCAid2hvaXMiOiB7ImNyZWF0ZWQiOiAiMjAxOS0xMi0xOCAxMzoxMDowMSIsICJ1cGRhdG'
                            'VkIjogIjIwMTktMTItMTkgMDQ6MDY6NTciLCAiZXhwaXJlcyI6ICIyMDIwLTEyLTE4IDEz'
                            'OjEwOjAxIiwgImFnZSI6IDI4MiwgInJlZ2lzdHJhciI6ICJPd25SZWdpc3RyYXIgSW5jIi'
                            'wgInJlZ2lzdHJhbnQiOiAidW5rbm93biIsICJoYXZlZGF0YSI6ICJ0cnVlIn19LCAic2Nv'
                            'cmUiOiB7InRvdGFsIjogMzIsICJzcmMiOiA2OC4zNSwgInRhZ3MiOiAwLjg5LCAiZnJlcX'
                            'VlbmN5IjogMC41NH0sICJmcCI6IHsiYWxhcm0iOiAiZmFsc2UiLCAiZGVzY3IiOiAiIn0s'
                            'ICJ0aHJlYXQiOiBbXSwgImlkIjogIjNjYjQ0ODg2LThlNjYtMzBjNi1hOGFhLTY2NTRjMG'
                            'I1NmQ0OSIsICJ0aXRsZSI6ICJSU1QgVGhyZWF0IGZlZWQuIElPQzogZGNoYW1iYW50b3Rh'
                            'LmNvbSIsICJkZXNjcmlwdGlvbiI6ICJJT0Mgd2l0aCB0YWdzOiBtYWx3YXJlIn0=',
                     'source.fqdn': 'dchambantota.com',
                     'source.ip': '111.221.46.75',
                     'time.source': '2020-10-06T00:00:00+00:00'
                     }]

with open(os.path.join(os.path.dirname(__file__), 'data2.json'), 'rb') as fh:
    RAW2 = base64.b64encode(fh.read()).decode()

REPORT2 = {"feed.name": "RSTThreats IP Feed",
           "raw": RAW2,
           "__type": "Report",
           }
EVENTS2 = {'__type': 'Event',
           'classification.type': 'malware',
           'extra.tags': ['generic'],
           'extra.threat_info': [],
           'feed.name': 'RSTThreats IP Feed',
           'source.ip': '116.108.249.75',
           'raw': 'eyJpcCI6IHsidjQiOiAiMTE2LjEwOC4yNDkuNzUiLCAibnVtIjogIjE5NTMyOTg3NjMifSwgImZzZWV'
                  'uIjogMTYwMDk5MjAwMCwgImxzZWVuIjogMTYwMTk0MjQwMCwgImNvbGxlY3QiOiAxNjAyMDI4ODAwL'
                  'CAidGFncyI6IHsic3RyIjogWyJnZW5lcmljIl0sICJjb2RlcyI6IFswXX0sICJhc24iOiB7Im51bSI'
                  '6IDc1NTIsICJmaXJzdGlwIjogeyJuZXR2NCI6ICIxMTYuMTA4LjI0OC4wIiwgIm51bSI6ICIxOTUzM'
                  'jk4NDMyIn0sICJsYXN0aXAiOiB7Im5ldHY0IjogIjExNi4xMDkuNzkuMjU1IiwgIm51bSI6ICIxOTU'
                  'zMzIwOTU5In0sICJjbG91ZCI6ICIiLCAiZG9tYWlucyI6IDQ5NzIyLCAib3JnIjogIlZpZXR0ZWwgR'
                  '3JvdXAiLCAiaXNwIjogIlZJRVRFTEFTQVAifSwgImdlbyI6IHsiY2l0eSI6ICJIbyBDaGkgTWluaCB'
                  'DaXR5IiwgImNvdW50cnkiOiAiVmlldG5hbSIsICJyZWdpb24iOiAiSG8gQ2hpIE1pbmgifSwgInJlb'
                  'GF0ZWQiOiB7ImRvbWFpbnMiOiBbXX0sICJzY29yZSI6IHsidG90YWwiOiAzNywgInNyYyI6IDU2LjE'
                  'yLCAidGFncyI6IDAuOCwgImZyZXF1ZW5jeSI6IDAuODN9LCAiZnAiOiB7ImFsYXJtIjogImZhbHNlI'
                  'iwgImRlc2NyIjogIiJ9LCAidGhyZWF0IjogW10sICJpZCI6ICJhNjFkMjFiOC1hZjVjLTM2MGItYmI'
                  '0MS0wYThlMjFiNzM1OGYiLCAidGl0bGUiOiAiUlNUIFRocmVhdCBmZWVkLiBJT0M6IDExNi4xMDguM'
                  'jQ5Ljc1IiwgImRlc2NyaXB0aW9uIjogIklPQyB3aXRoIHRhZ3M6IGdlbmVyaWMifQ==',
           'time.source': '2020-10-06T00:00:00+00:00'
           }


with open(os.path.join(os.path.dirname(__file__), 'data3.json'), 'rb') as fh:
    RAW3 = base64.b64encode(fh.read()).decode()

REPORT3 = {"feed.name": "RSTThreats URL Feed",
           "raw": RAW3,
           "__type": "Report",
           }
EVENTS3 = {'__type': 'Event',
           'classification.type': 'malware',
           'extra.tags': ['malware'],
           'extra.threat_info': [],
           'feed.name': 'RSTThreats URL Feed',
           'raw': 'eyJ1cmwiOiAiMTE0LjIzNC4xNjYuMjU1OjM5NDM2L21vemkuYSIsICJmc2VlbiI6IDE1OTg5MTg0MDA'
                  'sICJsc2VlbiI6IDE2MDE5NDI0MDAsICJjb2xsZWN0IjogMTYwMjAyODgwMCwgInRhZ3MiOiB7InN0ci'
                  'I6IFsibWFsd2FyZSJdLCAiY29kZXMiOiBbMTBdfSwgInNjb3JlIjogeyJ0b3RhbCI6IDEwLCAic3JjI'
                  'jogNzMuMDYsICJ0YWdzIjogMC44OSwgImZyZXF1ZW5jeSI6IDAuNTh9LCAicmVzb2x2ZWQiOiB7InN0'
                  'YXR1cyI6IDUwM30sICJmcCI6IHsiYWxhcm0iOiAidHJ1ZSIsICJkZXNjciI6ICJSZXNvdXJjZSB1bmF'
                  '2YWlsYWJsZSJ9LCAidGhyZWF0IjogW10sICJpZCI6ICI5ODdmNTAzOC0yOThmLTM3ZWItYTFkNS1hMT'
                  'cxMDVmNmI0YjUiLCAidGl0bGUiOiAiUlNUIFRocmVhdCBmZWVkLiBJT0M6IDExNC4yMzQuMTY2LjI1N'
                  'TozOTQzNi9tb3ppLmEiLCAiZGVzY3JpcHRpb24iOiAiSU9DIHdpdGggdGFnczogbWFsd2FyZSJ9',
           'time.source': '2020-10-06T00:00:00+00:00',
           'source.url': 'http://114.234.166.255:39436/mozi.a'
           }


class TestJSONCustomParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a JSONCustomParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = JSONCustomParserBot

    def test_report_1(self):
        """ Test if correct Event has been produced. """
        self.input_message = MULTILINE_REPORT
        self.sysconfig = {"splitlines": True,
                          "type": "malware",
                          "time_format": "epoch_millis",
                          "translate_fields": {"source.fqdn": "domain",
                                               "time.source": "lseen",
                                               "extra.tags": "tags.str",
                                               "extra.threat_info": "threat",
                                               "source.ip": "resolved.ip.a"
                                               }
                          }
        self.run_bot()
        self.assertMessageEqual(0, MULTILINE_EVENTS[0])
        self.assertMessageEqual(1, MULTILINE_EVENTS[1])

    def test_report_2(self):
        """ Test if correct Event has been produced. """
        self.input_message = REPORT2
        self.sysconfig = {"splitlines": True,
                          "type": "malware",
                          "time_format": "epoch_millis",
                          "translate_fields": {"source.ip": "ip.v4",
                                               "time.source": "lseen",
                                               "extra.tags": "tags.str",
                                               "extra.threat_info": "threat"
                                               }
                          }
        self.run_bot()
        self.assertMessageEqual(0, EVENTS2)

    def test_report_3(self):
        """ Test if correct Event has been produced. """
        self.input_message = REPORT3
        self.sysconfig = {"splitlines": True,
                          "type": "malware",
                          "time_format": "epoch_millis",
                          "translate_fields": {"source.url": "url",
                                               "time.source": "lseen",
                                               "extra.tags": "tags.str",
                                               "extra.threat_info": "threat"
                                               }
                          }
        self.run_bot()
        self.assertMessageEqual(0, EVENTS3)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
