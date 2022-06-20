# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.threatfox.parser import ThreatfoxParserBot

with open(os.path.join(os.path.dirname(__file__), 'data.json'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

REPORT = {"time.observation": "2022-06-17T13:13:10+00:00",
          "raw": RAW,
          "__type": "Report",
          "feed.url": "https://threatfox-api.abuse.ch/api/v1/",
          "feed.name": "Threatfox Meta",
          "feed.provider": "Threatfox",
          "feed.accuracy": 100.0
          }
EVENT = {'__type': 'Event',
         "feed.accuracy": 100.0, 
         "feed.name": "Threatfox Meta", 
         "feed.provider": "Threatfox", 
         "feed.url": "https://threatfox-api.abuse.ch/api/v1/", 
         "time.observation": "2022-06-17T17:18:15+00:00",
         "malware.hash.sha256": "904b693370bd0fe9427c00de8520925c0ef4ccd85b4b9730590780dd3ac9ca1b", 
         "malware.name": "win.emotet",
         "extra.tags": ["epoch4", "exe"], 
         "time.source": "2022-06-17T15:08:51+00:00", 
         "extra.ioc_type": "sha256_hash", 
         "extra.id": "716085", 
         "extra.threat_type": "payload", 
         "extra.malware_alias": ["Geodo", "Heodo"], 
         "extra.confidence_level": 75, 
         "extra.reporter": "Cryptolaemus1", 
         "classification.type":"malware", 
         "raw":"eyJpZCI6ICI3MTYwODUiLCAiaW9jIjogIjkwNGI2OTMzNzBiZDBmZTk0MjdjMDBkZTg1MjA5MjVjMGVmNGNjZDg1YjRiOTczMDU5MDc4MGRkM2FjOWNhMWIiLCAidGhyZWF0X3R5cGUiOiAicGF5bG9hZCIsICJ0aHJlYXRfdHlwZV9kZXNjIjogIkluZGljYXRvciB0aGF0IGlkZW50aWZpZXMgYSBtYWx3YXJlIHNhbXBsZSAocGF5bG9hZCkiLCAiaW9jX3R5cGUiOiAic2hhMjU2X2hhc2giLCAiaW9jX3R5cGVfZGVzYyI6ICJTSEEyNTYgaGFzaCBvZiBhIG1hbHdhcmUgc2FtcGxlIChwYXlsb2FkKSIsICJtYWx3YXJlIjogIndpbi5lbW90ZXQiLCAibWFsd2FyZV9wcmludGFibGUiOiAiRW1vdGV0IiwgIm1hbHdhcmVfYWxpYXMiOiAiR2VvZG8sSGVvZG8iLCAibWFsd2FyZV9tYWxwZWRpYSI6ICJodHRwczovL21hbHBlZGlhLmNhYWQuZmtpZS5mcmF1bmhvZmVyLmRlL2RldGFpbHMvd2luLmVtb3RldCIsICJjb25maWRlbmNlX2xldmVsIjogNzUsICJmaXJzdF9zZWVuIjogIjIwMjItMDYtMTcgMTU6MDg6NTEgVVRDIiwgImxhc3Rfc2VlbiI6ICIyMDIyLTA2LTE3IDE1OjEyOjE3IFVUQyIsICJyZWZlcmVuY2UiOiBudWxsLCAicmVwb3J0ZXIiOiAiQ3J5cHRvbGFlbXVzMSIsICJ0YWdzIjogWyJlcG9jaDQiLCAiZXhlIl19"
         }

class TestThreatfoxParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ThreatfoxParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ThreatfoxParserBot

    def test_sample(self):
        """ Test if correct Event has been produced. """
        self.input_message = REPORT
        self.sysconfig = {}
        self.run_bot()
        self.assertMessageEqual(0, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
