#!/bin/env python

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
                hostvars=dict(type='dict', required=True),
                port=dict(required=False, default=22),
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
            'ip': ansible_arguments['hostvars']['inventory_hostname'],
            'port': ansible_arguments['hostvars']['port'],
            'username': ansible_arguments['hostvars']['ansible_use'],
            'password': ansible_arguments['hostvars']['ansible_password'],
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
        cmd = sys.argv[1] if len(sys.argv) > 1 else 'show image version'
    
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
        module.exit_json(**{
            'stdout': output,
            'stdout_lines': output.split('\n'),
        })
    else:
        print(output)

def main():
    run_module()


if __name__ == '__main__':
    main()
