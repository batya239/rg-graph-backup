#!/usr/bin/python
# -*- coding: utf8


def dict_hash1(aDict):
    """
    hash from dictionary where key is hashable
    """
    h = 0
    for p in aDict.items():
        h += hash(p)
    return h


class frozendict(dict):
    def __setitem__(self, key, value):
        raise AssertionError, 'this is immutable dictionary'

    def __hash__(self):
        items = self.items()
        res = hash(items[0])
        for item in items[1:]:
            res ^= hash(item)
        return res

