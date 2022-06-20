"""
ThreatfoxParserBot
Retrieves a base64 encoded JSON-String from raw and converts it into an
event.

"""
from intelmq.lib.bot import Bot
from intelmq.lib.utils import base64_decode
from datetime import datetime
import json


class ThreatfoxParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = base64_decode(report["raw"])
        result = json.loads(raw_report)
        for feed in result["data"]:
            event = self.new_event(report)
            if(feed["ioc_type"] == "sha256_hash"):
                event.add('malware.hash.sha256', feed["ioc"])
            elif(feed["ioc_type"] == "ip:port"):
                event.add('source.ip', feed["ioc"].split(":")[0])
            elif(feed["ioc_type"] == "domain"):
                event.add('source.fqdn', feed["ioc"])
            elif(feed["ioc_type"] == "url"):
                event.add('source.url', feed["ioc"])
            elif(feed["ioc_type"] == "md5_hash"):
                event.add('malware.hash.md5', feed["ioc"])
            elif(feed["ioc_type"] == "sha1_hash"):
                event.add('malware.hash.sha1', feed["ioc"])
            event.add('malware.name', feed["malware"])
            event.add('extra.tags', feed["tags"])
            event.add('time.source', feed["first_seen"])
            event.add("extra.ioc_type", feed["ioc_type"])
            event.add("extra.id", feed["id"])
            event.add("extra.threat_type", feed["threat_type"])
            event.add("extra.malware_alias", feed["malware_alias"].split(","))
            event.add("extra.confidence_level", feed["confidence_level"])
            event.add("extra.reporter", feed["reporter"])
            event.add("extra.reference", feed["reference"])
            event.add("classification.type", 'malware')
            event.add("raw", json.dumps(feed))
            self.send_message(event)
            self.logger.info('Message was sent successfully.')
        self.acknowledge_message()
        


BOT = ThreatfoxParserBot
