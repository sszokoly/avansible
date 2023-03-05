from __future__ import print_function

debug_mode = False

if not debug_mode:
    from ansible.module_utils.basic import *
else:
    import sys

import re
from subprocess import Popen, PIPE


def get_certs(host, port, starttls=None):
    cmd  = ["openssl", "s_client", "-showcerts"]
    cmd += ["-starttls", starttls] if starttls else []
    cmd += ["-connect", "{0}:{1}".format(host, port)]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    data, _ = p.communicate()
    certs = re.findall(
        b"(-----BEGIN CERTIFICATE-----.+?-----END CERTIFICATE-----)",
        data,
        re.M|re.S
    )
    return certs

def run_module():
    # Setting parameters for Ansible
    if not debug_mode:
        module = AnsibleModule(
            argument_spec=dict(
                name=dict(required=True),
                host=dict(required=True),
                port=dict(required=False, default=443),
                starttls=dict(required=False, default=None),
            )
        )
        ansible_arguments = module.params
        name = ansible_arguments['name']
        host = ansible_arguments['host']
        port = ansible_arguments['port']
        starttls = ansible_arguments['starttls']
    
    else:
        host = sys.argv[1]
        port = sys.argv[2]
        starttls = sys.argv[3] if len(sys.argv) >=4 else None
    
    certs = get_certs(host, port, starttls)
    certs = [x.decode('utf-8') for x in certs]

    if not debug_mode:
        module.exit_json(**{name: certs})
    else:
        print(certs)

def main():
    run_module()

if __name__ == "__main__":
    main()
