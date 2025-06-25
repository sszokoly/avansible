#!/usr/bin/python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import subprocess
import tempfile
from ansible.module_utils.basic import AnsibleModule


def run_expect_scp(module, src, dest, user, host, password, port):
    with tempfile.NamedTemporaryFile(delete=False, mode='w', prefix=f"{host}_", suffix='.tcl') as f:
        script_path = f.name
        f.write(f"""#!/usr/bin/expect -f
set timeout 3
spawn scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=60 -P {port} {src} {user}@{host}:{dest}
expect {{
    "assword:" {{
        send "{password}\\r"
    }}
}}

set done 0
while {{!$done}} {{
    expect {{
        -re ".*100%.*" {{
            puts "Transfer complete"
            set done 1
        }}
        timeout {{
            sleep 1
        }}
        eof {{
            puts "Reached EOF before seeing 100%"
            set done 1
        }}
    }}
}}""")

    os.chmod(script_path, 0o700)
    
    result = subprocess.run(["expect", script_path],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8',
                            universal_newlines=True)
    try:
        os.remove(script_path)
    except OSError:
        pass
    
    if result.returncode != 0:
        module.fail_json(msg="SCP failed",
                            stdout=result.stdout,
                            stderr=result.stderr)

    return dict(
        changed=True,
        stdout=result.stdout,
        stderr=result.stderr
    )

def main():
    module = AnsibleModule(
        argument_spec=dict(
            src=dict(type='str', required=True),
            dest=dict(type='str', required=True),
            host=dict(type='str', required=True),
            user=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True),
            port=dict(type='int', required=False, default=22),
        ),
        supports_check_mode=False
    )

    args = module.params
    result = run_expect_scp(module, args['src'], args['dest'], args['user'], args['host'], args['password'], args['port'])
    module.exit_json(**result)


if __name__ == '__main__':
    main()