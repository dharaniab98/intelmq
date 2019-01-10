# -*- coding: utf-8 -*-
from intelmq.lib.bot import Bot
from collections.abc import Mapping


class AddFieldExpertBot(Bot):

    def init(self):
        self.field_name = getattr(self.parameters, 'field-name')
        self.field_value = getattr(self.parameters, 'field-value')
        self.add_to_extra = getattr(self.parameters, 'add_to_extra', True)

    def process(self):
        event = self.receive_message()

        if self.add_to_extra:
            if 'extra' in event:
                extra = event['extra']
                if isinstance(extra, str):
                    try:
                        extra = loads(extra)
                    except:
                        pass
                if isinstance(extra, Mapping):
                    extra[self.field_name] = self.field_value
                else:
                    extra = {self.field_name: self.field_value}
                event.change('extra', extra)

            else:  # no extra add extra
                event.add('extra', {self.field_name: self.field_value})
        else:
            event.add(self.field_name, self.field_value)

        self.send_message(event)
        self.acknowledge_message()


BOT = AddFieldExpertBot
