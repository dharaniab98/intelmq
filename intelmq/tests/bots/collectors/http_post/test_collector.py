# -*- coding: utf-8 -*-
"""
Testing  HTTPPostCollectorBot collector
"""
import os

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import intelmq.bots.collectors.http_post.collector_http_post.py
