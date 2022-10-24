#!/usr/bin/env python

class FilterModule(object):
    def filters(self):
        return {
            'int2hex': self.int2hex,
        }

    def int2hex(self, intString):
        return hex(int(intString))