#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from datetime import datetime, timedelta
import logging

import singleton
from BaseProxyProvider import BaseProxyProvider
from CNProxy import CNProxyProvider


__title__ = 'massproxy'
__version__ = '0.1.0'
__author__ = 'Hanabi1224'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Hanabi1224'

@singleton.singleton
class ProxyProvider(BaseProxyProvider):
    def __init__(self):
        self.providers = []

    def refresh_proxies(self):
        if self.proxies and self.last_update_utc + timedelta(minutes=5) > datetime.utcnow():
            return
        proxies = []
        for provider in self.providers:
            for proxy in provider.get_proxies():
                proxies.append(proxy)

        self.proxies = set(proxies)
        self.last_update_utc = datetime.utcnow()
        logging.info('{0} unique proxies loaded.'.format(len(self.proxies)))

    def register_provider(self, provider):
        if provider and provider not in self.providers and isinstance(provider, BaseProxyProvider):
            self.providers.append(provider)
        else:
            logging.error('Error registering provider {0}'.format(provider))


__instance = ProxyProvider()
__instance.register_provider(CNProxyProvider())

get_proxies = __instance.get_proxies
get_proxies_iterator = __instance.get_proxies_iterator
get_proxy_for = __instance.get_unblocked_proxy_for
block_proxy_for = __instance.block_proxy_for
register_provider = __instance.register_provider

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    for proxy in get_proxies(3):
        print(proxy)

    print(get_proxy_for('http://www.bing.com/'))
