#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import logging

from BaseProxyProvider import BaseProxyProvider
import singleton


@singleton.singleton
class CNProxyProvider(BaseProxyProvider):
    def __init__(self):
        BaseProxyProvider.__init__(self)

    def __get_all_proxies(self):
        yield 'http://101.227.246.107:8118/'
        yield 'http://101.231.157.86/'
        yield 'http://101.255.28.38:8080/'


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    for proxy in CNProxyProvider().get_proxies():
        print(proxy)
        