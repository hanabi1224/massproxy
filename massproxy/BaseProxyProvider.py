#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from datetime import datetime, timedelta
import random
import threading
import os.path
import logging

import requests


DIR = os.path.dirname(os.path.dirname(__file__))


class BaseProxyProvider(object):
    def __init__(self):
        self.proxies = []

    def refresh_proxies(self):
        if self.proxies and self.last_update_utc + timedelta(minutes=30) > datetime.utcnow():
            return
        proxies = []
        self.cache_file_name = os.path.join(DIR, self.__class__.__name__ + '.proxycache')
        if not os.path.isfile(self.cache_file_name):
            self.__refresh_proxy_cache()
        elif datetime.utcfromtimestamp(os.path.getmtime(self.cache_file_name)) + timedelta(days=1) < datetime.utcnow():
            threading.Thread(target=self.__refresh_proxy_cache).start()

        with open(self.cache_file_name) as fp:
            for line in fp.xreadlines():
                line = line.strip()
                if line:
                    try:
                        proxies.append(line)
                    except Exception as e:
                        logging.error('Error parsing line {0}:{1}'.format(line, e))
        self.proxies = set(proxies)
        self.last_update_utc = datetime.utcnow()
        logging.info('{0} proxies loaded.'.format(len(self.proxies)))

    def get_proxies(self, max_count=0, target_url=None, random_result=True):
        self.refresh_proxies()
        need_validation = bool(target_url)
        result_set = []
        proxies = list(self.proxies)
        if random_result:
            random.shuffle(proxies)
        for proxy in proxies:
            if need_validation:
                try:
                    requests.get(target_url, proxies={'http': proxy}, timeout=10)
                except:
                    continue
            result_set.append(proxy)
            if max_count > 0 and max_count >= len(result_set):
                break
        return result_set

    def __get_all_proxies(self):
        pass

    def __refresh_proxy_cache(self):
        proxies = self.__get_all_proxies()
        if proxies:
            with open(self.cache_file_name, 'w') as fp:
                for proxy in proxies:
                    fp.write(proxy)
                    fp.write('\n')
            self.last_update_utc = datetime.min
            logging.info('Proxy list refreshed from provider {0}.'.format(self.__class__.__name__))