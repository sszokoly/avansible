#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from ansible.module_utils.basic import *
from subprocess import Popen, PIPE
import re

def getcerts(host, port, starttls=None):
    cmd = ["openssl", "s_client", "-showcerts"]
    cmd += ["-starttls", starttls] if starttls else []
    cmd += ["-connect", "{0}:{1}".format(host, port)]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    data = p.communicate()[0].decode("utf8")
    if p.returncode and not data:
        return []
    certs = re.findall(
        "(-----BEGIN CERTIFICATE-----.+?-----END CERTIFICATE-----)",
        data,
        re.M|re.S
    )
    return certs

def main():
    rv = {}
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True),
            port=dict(required=True),
            starttls=dict(required=False, default=None),
        ))
    certs = getcerts(
        module.params['host'],
        module.params['port'],
        module.params['starttls'],
        )
    rv['certs'] = certs
    module.exit_json(**rv)

if __name__ == "__main__":
    main()
