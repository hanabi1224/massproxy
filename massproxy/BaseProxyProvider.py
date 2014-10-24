#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from datetime import datetime, timedelta
import random
import re
import time
import threading
import os.path
import logging

try:
    import queue
except:
    import Queue as queue

import requests

DIR = os.path.dirname(os.path.dirname(__file__))

class BaseProxyProvider(object):
    block_list = {}

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

    def get_unblocked_proxy_for(self, url, need_validation=False):
        host = self.__get_host(url)
        available = []
        if need_validation:
            iterator = self.get_proxies_iterator(target_url=url)
        else:
            iterator = self.get_proxies_iterator()

        for proxy in iterator:
            blocker_key = '{0}:{1}'.format(proxy, host)
            if blocker_key not in self.block_list or self.block_list[blocker_key] < datetime.datetime.utcnow():
                if blocker_key in self.block_list:
                    try:
                        del self.block_list[blocker_key]
                    except:
                        pass
                return proxy

        logging.warning('No valid proxy found, retrying in 5 minutes...')
        time.sleep(5 * 60)
        return self.get_unblocked_proxy_for(url)

    def block_proxy_for(self, url, proxy, minutes=15):
        host = self.__get_host(url)
        self.block_list['{0}:{1}'.format(proxy, host)] = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=minutes)
        logging.info('blocking proxy {0} for domain {1}'.format(proxy, host))

    def __get_host(self, url):
        if url:
            m = re.match(r'https?://[^/]+?/', url, re.I)
            if m:
                return m.group()
        return None

    def get_proxies(self, max_count=0, target_url=None, random_result=True):
        return (p for p in self.get_proxies_iterator(max_count, target_url, random_result))

    def get_proxies_iterator(self, max_count=0, target_url=None, random_result=True):
        try:
            self.proxies
        except AttributeError:
            self.proxies = []

        self.refresh_proxies()
        need_validation = bool(target_url)
        proxies = list(self.proxies)
        if random_result:
            random.shuffle(proxies)
        count = 0
        for proxy in proxies:
            #TODO: Async validation
            if need_validation:
                try:
                    requests.get(target_url, proxies={'http': proxy}, timeout=10)
                except:
                    continue
            yield proxy
            count += 1
            if max_count > 0 and count >= max_count:
                return

    # def __validate_async(self, proxies, max_count, target_url, valid_proxy_list):
    #     task_queue = queue.Queue(min(32, max_count * 2 + 3))
    #     for proxy in proxies:
    #         task_queue.put()
    #
    # def __validate_proxy(self, proxy, target_url, valid_proxy_list):
    #     try:
    #         requests.get(target_url, proxies={'http': proxy}, timeout=10)
    #         valid_proxy_list.append(proxy)
    #     except:
    #         pass

    def _get_all_proxies(self):
        pass

    def __refresh_proxy_cache(self):
        print(self)
        proxies = self._get_all_proxies()
        if proxies:
            with open(self.cache_file_name, 'w') as fp:
                for proxy in proxies:
                    fp.write(proxy)
                    fp.write('\n')
            self.last_update_utc = datetime.min
            logging.info('Proxy list refreshed from provider {0}.'.format(self.__class__.__name__))