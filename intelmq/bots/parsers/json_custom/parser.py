# -*- coding: utf-8 -*-

from dateutil.parser import parse

from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Message, MessageFactory
from intelmq.lib.utils import base64_decode

TIME_CONVERSIONS = {'timestamp': DateTime.from_timestamp,
                    'windows_nt': DateTime.from_windows_nt,
                    'epoch_millis': DateTime.from_epoch_millis,
                    None: lambda value: parse(value, fuzzy=True).isoformat() + " UTC"}


class JSONCustomParserBot(Bot):

    def init(self):
        self.time_format = getattr(self.parameters, "time_format", None)
        if self.time_format not in TIME_CONVERSIONS.keys():
            raise InvalidArgument('time_format', got=self.time_format,
                                  expected=list(TIME_CONVERSIONS.keys()),
                                  docs='docs/Bots.md')

        self.translate_fields = getattr(self.parameters, 'translate_fields', {})
        self.split_lines      = getattr(self.parameters, 'splitlines', False)
        self.default_url_protocol = getattr(self.parameters, 'default_url_protocol', 'http://')
        self.classification_type = getattr(self.parameters, 'type')

    def flatten_json(self, json_object):
        out = {}

        def flatten(x, name='', separator='.'):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + separator)
            else:
                out[name[:-1]] = x

        flatten(json_object)
        return out

    def process(self):

        report = self.receive_message()

        if self.split_lines:
            lines = base64_decode(report['raw']).splitlines()
        else:
            lines = [base64_decode(report['raw'])]

        for line in lines:
            if not line:
                continue

            msg = Message.unserialize(line)
            flatten_msg = self.flatten_json(msg)
            custom_msg = {}

            for key in self.translate_fields:
                data = flatten_msg.get(self.translate_fields[key])

                if key in ["time.source", "time.destination"]:
                    try:
                        data = int(data)
                    except:
                        pass
                    data = TIME_CONVERSIONS[self.time_format](data)

                elif key.endswith('.url'):
                    if not data:
                        continue
                    if '://' not in data:
                        data = self.default_url_protocol + data

                custom_msg[key] = data

            custom_msgs = []

            if "source.ip" in custom_msg and type(custom_msg["source.ip"]) is list:
                for ip in custom_msg["source.ip"]:
                    new_msg = custom_msg.copy()
                    new_msg["source.ip"] = ip
                    custom_msgs.append(new_msg)
            else:
                custom_msgs = [custom_msg]
            for msg in custom_msgs:
                new_event = MessageFactory.from_dict(msg,
                                                     harmonization=self.harmonization,
                                                     default_type='Event')
                event = self.new_event(report)
                event.update(new_event)

                if self.classification_type and "classification.type" not in event:
                    event.add('classification.type', self.classification_type)

                if 'raw' not in event:
                    event['raw'] = line
                self.send_message(event)

        self.acknowledge_message()


BOT = JSONCustomParserBot
