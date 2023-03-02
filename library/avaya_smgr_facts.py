#!/bin/env python

#from ansible.module_utils.basic import *
from subprocess import Popen, PIPE
from datetime import datetime
import re

def getcerts(host, port, starttls=None):
    cmd = ["openssl", "s_client", "-showcerts"]
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

def cert_attrs(cert):
    attrs = {}
    cmd = ["openssl", "x509", "-noout"]
    cmd += ["-subject", "-issuer", "-startdate", "-enddate", "-serial"]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    data = p.communicate(cert)[0].decode("utf-8")
    d = dict(x.split("=", 1) for x in data.split("\n") if x)
    for k in ['subject', 'issuer']:
        for attr in re.split('/', d[k].strip("/ \n")):
            k2,v2 = attr.split("=")
            attrs.setdefault(k, {}).update({k2.strip(): v2.strip()})
    for k in ['notBefore', 'notAfter']:
        attrs[k] = datetime.strptime(d[k], "%b %d %H:%M:%S %Y %Z")
    attrs['serial'] = d['serial']
    return attrs

def main():
    hosts = ['10.10.48.200', '10.10.48.200', '10.10.48.200']
    ports = [443, 52233, 5432]
    starttlss = ['', '', 'postgres']
    for host, port, starttls in zip(hosts, ports, starttlss):  
        cert = getcerts(host, port, starttls)[0]
        print(cert_attrs(cert))

if __name__ == "__main__":
    main()
