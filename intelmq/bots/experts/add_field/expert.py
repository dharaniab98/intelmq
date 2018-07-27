# -*- coding: utf-8 -*-
from intelmq.lib.bot import Bot


class AddFieldExpertBot(Bot):

    def init(self):
        self.field_name = getattr(self.parameters, 'field-name')
        self.field_value = getattr(self.parameters, 'field-value')

    def process(self):
        event = self.receive_message()

        if 'extra' in event:
            extra = event['extra']
            extra[self.field_name] = self.field_value
            event.change('extra', extra)

        else:
            event.add('extra', {self.field_name: self.field_value})

        self.send_message(event)
        self.acknowledge_message()


BOT = AddFieldExpertBot
