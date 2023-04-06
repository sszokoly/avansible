#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re

class FilterModule(object):
    '''Split a PEM with multiple certificates into a list of certificates'''

    def filters(self):
        return {
            'split_pem': self.split_pem
        }

    def split_pem(self, pem_data):
        if isinstance(pem_data, bytes):
            pem_data = pem_data.decode('utf-8')

        return re.findall(
            '(-----BEGIN CERTIFICATE-----.+?-----END CERTIFICATE-----)',
            pem_data,
            re.DOTALL
        )
