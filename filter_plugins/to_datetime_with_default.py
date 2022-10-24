#!/usr/bin/env python

import datetime

class FilterModule(object):
    def filters(self):
        return {
            'to_datetime_with_default': self.to_datetime_with_default,
        }

    def to_datetime_with_default(self, string, format="%Y-%m-%d %H:%M:%S", default=""):
        try:
            return datetime.datetime.strptime(string, format)
        except:
            return default
