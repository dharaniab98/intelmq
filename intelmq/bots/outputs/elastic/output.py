# -*- coding: utf-8 -*-

from json import loads
from collections.abc import Mapping

from elasticsearch import Elasticsearch

from intelmq.lib.bot import Bot


def replace_keys(obj, key_char='.', replacement='_'):
    if isinstance(obj, Mapping):
        replacement_obj = {}
        for key, val in obj.items():
            replacement_key = key.replace(key_char, replacement)
            replacement_obj[replacement_key] = replace_keys(val, key_char, replacement)
        return replacement_obj
    return obj


class ElasticsearchOutputBot(Bot):

    def init(self):
        self.elastic_host = getattr(self.parameters,
                                    'elastic_host', '127.0.0.1')
        self.elastic_port = getattr(self.parameters,
                                    'elastic_port', '9200')
        self.elastic_index = getattr(self.parameters,
                                     'elastic_index', 'intelmq')
        self.elastic_doctype = getattr(self.parameters,
                                       'elastic_doctype', 'events')
        self.replacement_char = getattr(self.parameters,
                                        'replacement_char', '_')
        self.flatten_fields = getattr(self.parameters,
                                      'flatten_fields', [])
        if isinstance(self.flatten_fields, str):
            self.flatten_fields = self.flatten_fields.split(',')

        self.bulk_process_chunk = getattr(self.parameters,
                                      'bulk_process_chunk', 1000)
        self.es = Elasticsearch([{'host': self.elastic_host,
                                  'port': self.elastic_port}])
        if not self.es.indices.exists(self.elastic_index):
            self.es.indices.create(index=self.elastic_index, ignore=400)

    def process(self):
        if self.msg_queue_count() > self.bulk_process_chunk:
            self.process_bulk()
        else:
            self.process_single()

    def process_bulk(self):
        events = []
        count = 0
        while count < self.bulk_process_chunk:
            event = self.receive_message()
            event_dict = event.to_dict(hierarchical=False)

            for field in self.flatten_fields:
                if field in event_dict:
                    val = event_dict[field]
                    # if it string try to convert to json
                    if isinstance(val, str):
                        try:
                            val = loads(val)
                        except:
                            pass
                    if isinstance(val, Mapping):
                        for key, value in val.items():
                            event_dict[key] = value
                        event_dict.pop(field)

            event_dict = replace_keys(event_dict,
                                      replacement=self.replacement_char)
            op = {"index": {}}
            events.append(op)
            self.logger.info("event dict: %s"%event_dict)
            events.append(event_dict)
            self.acknowledge_message()
            count += 1

        self.es.bulk(index=self.elastic_index,
                     doc_type=self.elastic_doctype,
                     refresh = True,
                     body=events)


    def process_single(self):
        event = self.receive_message()
        event_dict = event.to_dict(hierarchical=False)

        for field in self.flatten_fields:
            if field in event_dict:
                val = event_dict[field]
                # if it string try to convert to json
                if isinstance(val, str):
                    try:
                        val = loads(val)
                    except:
                        pass
                if isinstance(val, Mapping):
                    for key, value in val.items():
                        event_dict[key] = value
                    event_dict.pop(field)

        event_dict = replace_keys(event_dict,
                                  replacement=self.replacement_char)

        self.es.index(index=self.elastic_index,
                      doc_type=self.elastic_doctype,
                      body=event_dict)
        self.acknowledge_message()


BOT = ElasticsearchOutputBot
