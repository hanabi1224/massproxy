#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import logging
import re

import requests

from bs4 import BeautifulSoup

from BaseProxyProvider import BaseProxyProvider
import singleton


@singleton.singleton
class CNProxyProvider(BaseProxyProvider):
    def _get_all_proxies(self):
        for i in range(1, 12):
            try:
                url = 'http://www.cnproxy.com/proxy{0}.html'.format(i)
                r = requests.get(url)
                soup = BeautifulSoup(r.text)
                script_block = soup.find('head').find('script')
                pairs = {}
                for m in re.findall(r'(?P<k>\w)\="(?P<v>\d)"', script_block.text):
                    pairs[m[0]] = int(m[1])
                for tr in soup.find('div', id='proxylisttb').find_all('table')[-1].find_all('tr')[1:]:
                    td_list = tr.find_all('td')
                    schema = td_list[1].text.strip().lower()
                    if schema[:4] != 'http':
                        logging.info('Skipping unsupported proxy schema {0}'.format(schema))
                        continue
                    host = str(list(td_list[0].children)[0])
                    print(host)
                    port_text = td_list[0].find('script').text
                    port_text = port_text[port_text.index('+'):-1].replace('+', '')
                    port = ''
                    for ch in port_text:
                        port += str(pairs[ch])
                    port = int(port)
                    yield '{0}://{1}:{2}/'.format(schema, host, port)

            except Exception as e:
                logging.error(e)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    for proxy in CNProxyProvider().get_proxies():
        print(proxy)
        