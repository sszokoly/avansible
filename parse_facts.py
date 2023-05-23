#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
#############################################################################
## Name: parse_facts.py
## Parses yaml file from facts directory
## Date: 2023-03-23
## Version: 0.1
## Author: sszokoly@netagen.com
#############################################################################
"""
import os
import sys
import yaml
from utils.certificate_info import certificate_info

FACTS_CACHE = "facts_cache"

def certificates(facts):
    pems = facts.get('certificates', None)
    certs = {}
    if not pems:
        return None
    for service, pem_list in pems.items():
        if not pem_list:
            continue
        certs.update({service: certificate_info(pem_list[0])})
    return certs

def main(facts_cache):
    files = os.listdir(facts_cache)
    for file in files:
        with open(os.path.join(facts_cache, file), 'r') as fd:
            facts = yaml.safe_load(fd)
            group_names = facts.get('group_names', None)
            if not group_names:
                continue
            ansible_parent_group, ansible_child_group = group_names
            certs = certificates(facts)
            if not certs:
                print (ansible_parent_group, "", "") 
            else:
                for service, cert_attribs in certs.items():
                    if not cert_attribs:
                        continue
                    print(file, ansible_parent_group, ansible_child_group, service, cert_attribs)

if __name__ == "__main__":
    facts_cache = sys.argv[1] if len(sys.argv) > 1 else FACTS_CACHE
    sys.exit(main(facts_cache))
