# -*- coding: utf-8 -*-
import json

from intelmq.bots.experts.apnic_rdap.lib import APNIC
from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache
from intelmq.lib.harmonization import IPAddress

MINIMUM_BGP_PREFIX_IPV4 = 24
MINIMUM_BGP_PREFIX_IPV6 = 128


class APNICExpertBot(Bot):

    def init(self):
        self.cache = Cache(self.parameters.redis_cache_host,
                           self.parameters.redis_cache_port,
                           self.parameters.redis_cache_db,
                           self.parameters.redis_cache_ttl,
                           getattr(self.parameters, "redis_cache_password",
                                   None)
                           )
        self.bypass = getattr(self.parameters, "bypass", False)
        self.timeout = self.parameters.http_timeout_sec

    def process(self):
        event = self.receive_message()

        if self.bypass:
            self.send_message(event)
        else:
            ip_key = "source.ip"
            network_key = "source.network"

            if ip_key not in event and network_key not in event:
                self.send_message(event)
            else:
                if ip_key in event:
                    ip = event.get(ip_key)
                    query_str = ip

                if network_key in event:         # network preferred over ip
                    netw = event.get(network_key)
                    ip = netw.split('/')[0]
                    prefix = int(netw.split('/')[1])
                    query_str = netw

                ip_version = IPAddress.version(ip)
                ip_integer = IPAddress.to_int(ip)

                if ip_version == 4:
                    minimum = MINIMUM_BGP_PREFIX_IPV4
                elif ip_version == 6:
                    minimum = MINIMUM_BGP_PREFIX_IPV6
                else:
                    raise ValueError('Unexpected IP version '
                                     '{!r}.'.format(ip_version))

                if network_key in event:
                    cache_key = bin(ip_integer)[2: minimum + 2] + bin(prefix)[2:]
                elif ip_key in event:
                    cache_key = bin(ip_integer)[2: minimum + 2]

                result_json = self.cache.get(cache_key)

                if result_json:
                    result = json.loads(result_json)
                else:
                    result = APNIC.query(query_str, self.timeout)
                    if result:
                        result_json = json.dumps(result)
                        self.cache.set(cache_key, result_json)

                for result_key, result_value in result.items():
                    event.add('extra.%s' % result_key, result_value, overwrite=True)

                self.send_message(event)

        self.acknowledge_message()


BOT = APNICExpertBot
