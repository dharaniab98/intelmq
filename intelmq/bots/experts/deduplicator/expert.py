# -*- coding: utf-8 -*-
"""Deduplicator expert bot

Parameters:

    redis_cache_host: string

    redis_cache_port: int

    redis_cache_db: int

    redis_cache_ttl: int

    redis_cache_password: string.  default: {None}

    filter_type: string ["blacklist", "whitelist"]

    bypass: boolean default: False

    filter_keys: string with multiple keys separated by comma. Please
                 note that time.observation key is never consider by the
                 system because system will always ignore this key.
"""

from datetime import datetime as dt
from dateutil import relativedelta

from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache


class DeduplicatorExpertBot(Bot):

    _message_processed_verb = 'Forwarded'

    def init(self):
        self.cache = Cache(self.parameters.redis_cache_host,
                           self.parameters.redis_cache_port,
                           self.parameters.redis_cache_db,
                           self.parameters.redis_cache_ttl,
                           getattr(self.parameters, "redis_cache_password",
                                   None)
                           )
        self.filter_keys = {k.strip() for k in
                            self.parameters.filter_keys.split(',')}
        self.bypass = getattr(self.parameters, "bypass", False)
        self.month_based = getattr(self.parameters, "month_based", False)
        self.persist_duplicate = getattr(self.parameters, "persist_duplicate", False)

    def process(self):
        message = self.receive_message()

        if self.bypass:
            self.send_message(message)
        else:
            message_hash = message.hash(filter_keys=self.filter_keys,
                                        filter_type=self.parameters.filter_type)

            if not self.cache.exists(message_hash):
                if self.month_based:
                    next_month = dt.utcnow() + relativedelta.relativedelta(months=1)
                    cache_ttl = int((dt(next_month.year, next_month.month, 1) - dt.utcnow()).total_seconds())
                    self.cache.set(message_hash, 'hash', cache_ttl)
                else:
                    self.cache.set(message_hash, 'hash')
                self.send_message(message)
            else:
                if self.persist_duplicate:
                    self.cache.set(message_hash, 'hash')
                self.logger.debug('Dropped message.')

        self.acknowledge_message()


BOT = DeduplicatorExpertBot
