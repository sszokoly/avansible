#!/usr/bin/env python

class FilterModule(object):
    def filters(self):
        return {
            'int2hexstr': self.int2hexstr,
        }

    def int2hexstr(self, intString, default=""):
        try:
            return str(hex(int(intString)))
        except:
            return default
