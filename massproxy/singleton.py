#!/usr/bin/env python
# -*- coding: utf-8 -*-

def singleton(cls):
    instance_cache = {}

    def get_instance(*args, **kwds):
        return instance_cache.setdefault(cls, cls(*args, **kwds))

    return get_instance
