# -*- coding: utf-8 -*-

import requests
import json

QUERY = "http://rdap.apnic.net/ip/%s"


class APNIC():

    @staticmethod
    def query(query_str, timeout):

        result = {}
        try:
            text = requests.get(QUERY % (query_str), timeout=timeout).text
        except:         # Too many redirects error
            return result

        if not text:
            return result

        try:
            data = json.loads(text)
        except:         # Not Found or json loads error
            return result

        abuse = set()
        email = set()

        if "errorCode" not in data and "entities" in data:
            for entity in data['entities']:
                if 'entities' in entity:
                    for entity1 in entity['entities']:
                        if 'vcardArray' in entity1:
                            for arr in entity1['vcardArray'][1]:
                                if 'email' in arr:
                                    if 'abuse' in entity1['roles'] or 'abuse' in arr[3]:
                                        abuse.add(arr[3])
                                    else:
                                        email.add(arr[3])

                if 'vcardArray' in entity:
                    for arr in entity['vcardArray'][1]:
                        if 'email' in arr:
                            if 'abuse' in entity['roles'] or 'abuse' in arr[3]:
                                abuse.add(arr[3])
                            else:
                                email.add(arr[3])

        if abuse:
            result['abuse'] = list(abuse)

        if email:
            result['email']  = list(email)

        return result