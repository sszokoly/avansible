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

FACTS_CACHE = "facts_cache"

def main(facts_cache):
    files = os.listdir(facts_cache)
    for file in files:
        with open(os.path.join(facts_cache, file), 'r') as fd:
            facts = yaml.safe_load(fd)
            print(facts.keys())

if __name__ == "__main__":
    facts_cache = sys.argv[1] if len(sys.argv) > 1 else FACTS_CACHE
    sys.exit(main(facts_cache))
