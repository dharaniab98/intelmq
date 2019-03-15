# -*- coding: utf-8 -*-
import requests
import json

from intelmq.lib.bot import Bot


class TalosExpertBot(Bot):

    def process(self):
        event = self.receive_message()
        ip = event.get("source.ip")
        headers = {"user-agent": "Mozilla/5.0 Safari/537.36"}
        headers["referer"] = "https://talosintelligence.com/reputation_center/lookup?search=" + ip
        url = "https://www.talosintelligence.com/sb_api/query_lookup?query=%2Fapi%2Fv2%2Fdetails%2Fip%2F&query_entry="
        res = requests.get(url=url + ip, headers=headers).text
        data = json.loads(res)
        if data['daily_spam_name'] in ['High', 'Very High', 'Critical']:
            event.add('extra.tag', 'spam')
        for blacklist in ['cbl.abuseat.org', 'pbl.spamhaus.org', 'sbl.spamhaus.org', 'bl.spamcop.net']:
            if data['blacklists'][blacklist]['rules']:
                event.add('extra.tag', 'blacklist', overwrite=True)
                break
        self.send_message(event)
        self.acknowledge_message()


BOT = TalosExpertBot
