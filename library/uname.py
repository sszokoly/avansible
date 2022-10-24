#!/usr/bin/python
from ansible.module_utils.basic import *

def main():      
    rv = {}
    module = AnsibleModule(argument_spec={})      
    rc, out, err = module.run_command(['/usr/bin/uname', '-r'])
    rv['uname'] = out.split()
    module.exit_json(**rv)

if __name__ == "__main__":
    main()    
