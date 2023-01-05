
#!/bin/env python

# Copyright 2023 Sabi Szokoly <sszokoly@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DOCUMENTATION = r'''
---
module: avaya_bgw_raw

short_description: Retrieves command output from Avaya Branch Gateway

version_added: "0.0.1"

description:
    - Retrieves command output from Avaya Branch Gateway via raw SSH connection

requirements:
    - netmiko

options:
    host:
        description:
            - Typically set to {{ ansible_host }}
        required: true
        type: str
    port:
        description:
            - Typically set to {{ ansible_port }}, default 22 if omitted
        required: false
        type: int
    username:
        description:
            - Typically set to {{ ansible_user }}
        required: true
        type: str
    password:
        description:
            - Typically set to {{ ansible_ssh_pass }}
        required: true
        type: str
    cmd:
        description:
            - The command to run on the Branch Gateway
        required: true
        type: str
author:
    - Sabi Szokoly (sszokoly@gmail.com)
'''

EXAMPLES = r'''
# Retrieve the output of a command from Branch Gateway through controller
- name: Obtain `show image version` from G450
    avaya_bgw_raw:
        host: "{{ ansible_host }}"
        username: "{{ ansible_user }}"
        password: "{{ ansible_ssh_pass }}"
        cmd: "show image version"
    delegate_to: localhost
    no_log: true
'''

RETURNS = r'''
# Returns output as string and list of lines.
stdout:
    description: output of lines already stripped of page delimiter
    type: str
    returned: always
    sample: "Bank         Version\n-----------  -------\nA (current)  41.35.0\nB            41.34.4"
stdout_lines:
    description: list of lines of output, already stripped of page delimiter
    type: list
    returned: always
    sample: [
        "Bank         Version",
        "-----------  -------",
        "A (current)  41.35.0",
        "B            41.34.4"
    ]
'''

# Set to True if running outside of Ansible
debug_mode = False

if not debug_mode:
    from ansible.module_utils.basic import *
else:
    import sys

try:
    from netmiko import ConnectHandler
    has_netmiko = True
except:
    has_netmiko = False

def run_module():
    # Setting parameters for Ansible
    if not debug_mode:
        module = AnsibleModule(
            argument_spec=dict(
                host=dict(required=True),
                port=dict(required=False, default=22),
                username=dict(required=True),
                password=dict(required=True),
                cmd=dict(required=True)
            )
        )
        ansible_arguments = module.params
    
    # Checking if netmiko is installed
    if not has_netmiko:
        if not debug_mode:
            module.fail_json(msg='Missing Netmiko module')
        else:
            print('Missing Netmiko module')

    # Porting the Ansible arguments into Netmiko
    if not debug_mode:
        bgw = {
            'device_type': 'avaya_vsp',
            'ip': ansible_arguments['host'],
            'port': ansible_arguments['port'],
            'username': ansible_arguments['username'],
            'password': ansible_arguments['password'],
        }
        cmd = ansible_arguments['cmd']

    # Debug mode, running outside of Ansible
    else:
        bgw = {
            'device_type': 'avaya_vsp',
            'ip': '10.10.48.58',
            'port': str(22),
            'username': 'root',
            'password': 'R00t01',
        }
        cmd = sys.argv[1] if len(sys.argv) > 1 else 'show system'
    
    delimiter = '\n--type q to quit or space key to continue-- '
    prompt = '\(super\)# '
    expect_string = '|'.join((delimiter, prompt))
    
    try:
        handler = ConnectHandler(**bgw)
    except Exception as err:
        if not debug_mode:
            module.fail_json(msg=str(err))
        else:
            print(str(err))
    
    output = handler.send_command(cmd, expect_string=expect_string)
    if delimiter in output:
        output += handler.send_command('\n', expect_string=expect_string)
    output = output.replace(delimiter, '')
    
    if not debug_mode:
        module.exit_json(**{'stdout': output, 'stdout_lines': output.split('\n')})
    else:
        print(output)

def main():
    run_module()


if __name__ == '__main__':
    main()
