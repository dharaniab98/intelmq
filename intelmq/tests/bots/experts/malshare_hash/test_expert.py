# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.malshare_hash.expert import MalshareHashExpertBot

EXAMPLE_INPUT_1 = {"__type": "Event",
                   "feed.url": "https://malshare.com/",
                   "time.observation": "2019-01-22T09:18:44+00:00",
                   "malware.hash.md5": "5a52e3733be29e661fbfb8707282e0c0",
                   "extra.file_type": "PE32",
                   "time.source": "2019-01-22T11:13:11+00:00",
                   "classification.type": "malware"
                   }
EXAMPLE_OUTPUT_1 = {"__type": "Event",
                    "feed.url": "https://malshare.com/",
                    "time.observation": "2019-01-22T09:18:44+00:00",
                    "malware.hash.md5": "5a52e3733be29e661fbfb8707282e0c0",
                    "extra.file_type": "PE32",
                    "time.source": "2019-01-22T11:13:11+00:00",
                    "classification.type": "malware",
                    "malware.hash.sha1": "f8aab562a37b045ff86c28ca319c98dd0daed23f",
                    "malware.hash.sha256": "f4cb402a8bf35658d940ccf73e6e72d716999d8970e6d4dfe5e820ed36abddaf",
                    "extra.yara_rules": "CuckooSandbox/vmdetect,YRP/possible_includes_base64_packed_functions,"
                                        "YRP/VC8_Microsoft_Corporation,YRP/Microsoft_Visual_Cpp_8,YRP/IsPE32,YRP/IsWindowsGUI,"
                                        "YRP/HasDebugData,YRP/HasRichSignature,YRP/maldoc_find_kernel32_base_method_1,"
                                        "YRP/domain,YRP/url,YRP/contentis_base64,YRP/Browsers,YRP/VM_Generic_Detection,"
                                        "YRP/VMWare_Detection,YRP/Misc_Suspicious_Strings,YRP/DebuggerException__SetConsoleCtrl,"
                                        "YRP/vmdetect,YRP/anti_dbg,YRP/escalate_priv,YRP/win_mutex,YRP/win_registry,YRP/win_token,"
                                        "YRP/win_files_operation,YRP/Advapi_Hash_API,YRP/CRC32_poly_Constant,YRP/CRC32_table,"
                                        "YRP/CRC32b_poly_Constant,YRP/MD5_Constants,YRP/RIPEMD160_Constants,YRP/SHA1_Constants,"
                                        "YRP/SHA512_Constants,YRP/DES_Long,YRP/RijnDael_AES,YRP/BASE64_table,YRP/spyeye_plugins,"
                                        "YRP/Str_Win32_Internet_API,YRP/Str_Win32_Http_API,YRP/GenerateTLSClientHelloPacket_Test"
                    }
EXAMPLE_INPUT_2 = {"__type": "Event",
                   "feed.url": "https://malshare.com/",
                   "time.observation": "2019-01-22T09:18:44+00:00",
                   "malware.hash.md5": "8334f23c935e688a10ca2ba1294d6a90",
                   "extra.file_type": "PE32",
                   "time.source": "2019-01-22T12:58:14+00:00",
                   "classification.type": "malware"
                   }
EXAMPLE_OUTPUT_2 = {"__type": "Event",
                    "feed.url": "https://malshare.com/",
                    "time.observation": "2019-01-22T09:18:44+00:00",
                    "malware.hash.md5": "8334f23c935e688a10ca2ba1294d6a90",
                    "extra.file_type": "PE32",
                    "time.source": "2019-01-22T12:58:14+00:00",
                    "classification.type": "malware",
                    "malware.hash.sha1": "bb421d4c4304f8ab5920acc01e525dbe8261b1d5",
                    "malware.hash.sha256": "11863185b39e13442504ec61639b78c16f2f4bc22ecad75abc2d0a0a39466d9c",
                    "source.url": "http://theubergroups.com/winos/emy.exe",
                    "extra.yara_rules": "YRP/IsPE32,YRP/IsWindowsGUI,YRP/IsBeyondImageSize,YRP/domain"
                    }
EXAMPLE_INPUT_3 = {"__type": "Event",
                   "feed.url": "https://malshare.com/",
                   "time.observation": "2019-01-22T09:18:44+00:00",
                   "malware.hash.md5": "c35aa07b62ba7b4e6ce1b5239cd23f3b",
                   "extra.file_type": "gzip",
                   "time.source": "2019-01-22T11:19:20+00:00",
                   "classification.type": "malware"
                   }
EXAMPLE_OUTPUT_3 = {"__type": "Event",
                    "feed.url": "https://malshare.com/",
                    "time.observation": "2019-01-22T09:18:44+00:00",
                    "malware.hash.md5": "c35aa07b62ba7b4e6ce1b5239cd23f3b",
                    "extra.file_type": "gzip",
                    "time.source": "2019-01-22T11:19:20+00:00",
                    "classification.type": "malware",
                    "malware.hash.sha1": "54cd7cf32de08fbffac162b64dc8cd11de0f5287",
                    "malware.hash.sha256": "ab07703590d128e48d6c226025d102b54d56fed1e4f74884cdd6d83f08d5e138",
                    "source.url": "http://www.gmpmfhkbkbeb.tw/ilmiqj/50225_780668.html"
                    }


class TestMalshareHashExpertBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = MalshareHashExpertBot

    def test_event_1(self):
        self.input_message = EXAMPLE_INPUT_1
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT_1)

    def test_event_2(self):
        self.input_message = EXAMPLE_INPUT_2
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT_2)

    def test_event_3(self):
        self.input_message = EXAMPLE_INPUT_3
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT_3)


if __name__ == '__main__':
    unittest.main
