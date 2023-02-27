#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
#############################################################################
## Name: inventory_from_smgr.py
## Creates an ANSIBLE inventory template from SMGR inventory
## Date: 2023-02-11
## Version: 0.1
## Author: sszokoly@netagen.com
#############################################################################
"""
from __future__ import print_function
try:
    import __builtin__
    input = raw_input
except:
    pass
import getpass
import socket
import sys
import time
try:
    import pwinput
    getpassword = pwinput.pwinput
except:
    getpassword = getpass.getpass
try:
    from paramiko.client import SSHClient, AutoAddPolicy
    has_paramiko = True
except:
    has_paramiko = False
from subprocess import Popen, PIPE

CMD = '''
mgmtia avmgmt -P pager=off --csv -c "
SELECT 
  app.name as name,
  systype.displaykey as type,
  dev.devicetypename as device_type,
  host.address as node
FROM rts_applicationsystem AS app
LEFT JOIN rts_host AS host ON app.host_id=host.id
LEFT JOIN rts_applicationsystemtype AS systype ON app.appsystemtypeid=systype.id
LEFT JOIN rts_devicetypes AS dev ON app.devicetypeid=dev.id
ORDER BY systype.name;"
'''
HEADER = "name,type,device_type,node"

def smgr_details():
    host = input("SMGR IP/FQDN:  ")
    cust_login = input("SMGR Username: ")
    cust_pass = getpassword("SMGR Password: ")
    root_pass = getpassword("Root Password: ")
    return host, cust_login, cust_pass, root_pass

def ssh_client_channel(host, username, password, root_password=None):
    if not has_paramiko:
        print("Paramiko library is not installed!")
        sys.exit(3)
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy)
    try:
        client.connect(host, username=username, password=password, timeout=5)
    except socket.timeout:
        print("Could not connect to {0}!".format(host))
        sys.exit(2)
    channel = client.invoke_shell()
    time.sleep(2)
    if root_password:
        channel.send('su -\n')
        time.sleep(0.5)
        channel.send(root_password + '\n')
        time.sleep(0.5)
        _ = channel.recv(2048)
    return client, channel

def smgr_inventory(host, username, password, root_password):
    if host:
        lines = []
        client, channel = ssh_client_channel(
            host,
            username,
            password,
            root_password
        )
        channel.send(CMD + '\n')
        time.sleep(1)
        while channel.recv_ready():
            lines.append(channel.recv(4096).decode('utf-8').replace('\r', ''))
            time.sleep(0.5)
        client.close()
        lines = ''.join(lines)
    else:
        if getpass.getuser() != 'root':
            print("You need root permissions to do this on a SMGR!")
            sys.exit(1)
        proc = Popen(CMD, shell=True, stdout=PIPE, stderr=PIPE)
        lines, _ = proc.communicate()
    start = lines.find(HEADER)
    end = lines.find('root >', start)
    lines = lines[start:end].strip().split('\n')
    return lines

def main():
    host, username, password, root_password = smgr_details()
    lines = smgr_inventory(
        host=host,
        username=username,
        password=password,
        root_password=root_password
    )
    print('\n'.join(lines))


if __name__ == "__main__":
    sys.exit(main())
