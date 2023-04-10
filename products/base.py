#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
#############################################################################
## Name: base.py
## Defines base product
## Date: 2023-04-07
## Version: 0.1
## Author: sszokoly@netagen.com
#############################################################################
"""
from __future__ import annotations
from dataclasses import dataclass, InitVar, field
from datetime import datetime

@dataclass
class CredentialInfo:
    name: str
    passwd_expires: str
    passwd_last_changed: str

@dataclass
class CredentialType:
    ssh: CredentialInfo()
    web: CredentialInfo()

class Base:
    def __init__(self, facts):
        self.facts = facts
        self.parent_group = facts.get("group_names", ["BASE"])[0]
        self.child_group = facts.get("group_names", ["", ""])[1]
        ssh = CredentialInfo("combat", "never", "never")
        web = CredentialInfo("", "", "")
        self.user =  CredentialType(ssh, web)


if __name__ == "__main__":
    aams = Base({
        "group_names": ["AAMS", "aams"],
        "users": {"ssh": {"combat": "Password expires: never"}, "web": {"admin": "Password expires: never"}}
    })
    print(aams.parent_group)
    print(aams.child_group)
    print(aams.user.ssh.passwd_expires)