#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
#############################################################################
## Name: certificate_info.py
## Extracts certificate info from a single PEM file
## Date: 2023-04-02
## Version: 0.1
## Author: sszokoly@netagen.com
#############################################################################
"""
import sys
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.x509.oid import ExtensionOID
from cryptography.hazmat.backends import default_backend

def load_pem_data(pem_data):
    pem_data = pem_data.encode() if isinstance(pem_data, str) else pem_data
    try:
        cert = x509.load_pem_x509_certificate(pem_data, backend=default_backend())
    except:
        print("PEM_DATA: {0}".format(pem_data))
        cert = None
    return cert

def get_subject_cn(cert):
    scns = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
    if scns:
        return scns[0].value
    return ""

def get_subject_o(cert):
    sos = cert.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)
    if sos:
        return sos[0].value
    return ""

def get_issuer_cn(cert):
    icns = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
    if icns:
        return icns[0].value
    return ""

def get_issuer_o(cert):
    ios = cert.issuer.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)
    if ios:
        return ios[0].value
    return ""

def get_san(cert):
    try:
        ext = cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
    except:
        return ""
    san_dns = [str(x) for x in ext.value.get_values_for_type(x509.DNSName)]
    san_ip = [str(x) for x in ext.value.get_values_for_type(x509.IPAddress)]
    return ','.join(san_dns + san_ip)

def certificate_info(pem_data):
    cert = load_pem_data(pem_data)

    return {
        'subject_cn': get_subject_cn(cert) if cert else "",
        'subject_o': get_subject_o(cert) if cert else "",
        'issuer_cn': get_issuer_cn(cert) if cert else "",
        'issuer_o': get_issuer_o(cert) if cert else "",
        'not_valid_before': cert.not_valid_before if cert else "",
        'not_valid_after': cert.not_valid_after if cert else "",
        'serial_number': hex(cert.serial_number) if cert else "",
        'subject_alternative_name': get_san(cert) if cert else "",
    }

if __name__ == "__main__":
    from pprint import pprint
    PEM_DATA = '-----BEGIN CERTIFICATE-----\nMIIEiTCCA3GgAwIBAgIUcvtUEZOYJGAfxcjVl4YPXOgfp/gwDQYJKoZIhvcNAQEL\nBQAwOzEaMBgGA1UEAwwRU3lzdGVtIE1hbmFnZXIgQ0ExDTALBgNVBAsMBE1HTVQx\nDjAMBgNVBAoMBUFWQVlBMB4XDTIyMDcyMTA1MDIzNloXDTI0MDcyMDA1MDIzNVow\nOjEbMBkGA1UEAwwSc20tc20xMDAubGFiLmxvY2FsMQ4wDAYDVQQKDAVBdmF5YTEL\nMAkGA1UEBhMCVVMwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCzPKz/\nDW53dwZIBuPQA/GayCIlBggwTdh7vAwjG0i7ewMyWyac3IuTtHr4Rr3GVy0ASjUu\np3DGFJMnH45CRB8AalolYDJ6Zv0iQoyWi4EPzxRF9ab0d8P3FTZiW5cJkr71rohK\nPz8BNxi08f8rHGKt7V0mnIPuVYHZ2bQIKtFaDQuo3KdSSztocZ7HNmSa9fyFSBXk\nM2liwUhiMjb6G5O666PMQpRR6800wgDJLLUK3E32CL854S1OtQP3MZcDulDUaATO\nyCgzII0W3VN0d/6zAXbtMcx7JQGnyifSpQpxixNAp2MauNfhmhvc+HMFT6D1LQN2\nK93nhKqTA6UVZD/hAgMBAAGjggGEMIIBgDAdBgNVHREEFjAUghJzbS1zbTEwMC5s\nYWIubG9jYWwwDAYDVR0TAQH/BAIwADAfBgNVHSMEGDAWgBReGhZFWhGyjqAR3Vew\nfUpNzBV/cjBOBggrBgEFBQcBAQRCMEAwPgYIKwYBBQUHMAGGMmh0dHA6Ly92c21n\nci5sYWIubG9jYWwvZWpiY2EvcHVibGljd2ViL3N0YXR1cy9vY3NwMA8GCSsGAQUF\nBzABBQQCBQAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMIGABgNVHR8E\neTB3MHWgc6Bxhm9odHRwOi8vdnNtZ3IubGFiLmxvY2FsL2VqYmNhL3B1YmxpY3dl\nYi93ZWJkaXN0L2NlcnRkaXN0P2NtZD1jcmwmaXNzdWVyPUNOPVN5c3RlbSUyME1h\nbmFnZXIlMjBDQSxPVT1NR01ULE89QVZBWUEwHQYDVR0OBBYEFGXnzLlOk3vjy99v\n2xHFK2khoag6MA4GA1UdDwEB/wQEAwID+DANBgkqhkiG9w0BAQsFAAOCAQEALhd2\nSrW9uRgdfhSob3NRhp0eXagXfswZ1UsLG1OyNDbkp1LvEOQmc9VjSUc39UkN8vLx\n6M9iTObme0QYZtcsVKxcJGIleFhBBSwSvn0Otmh+OKO2mBOngHDOSE+peynhXMGd\n1vxwJsdWQExcVQb6bHqwUXHCeXYHYnAzS8rZqZDgPG6BXSR7UHLdKUIfu8qIkuuZ\n3VNlx9PZ3uaYpIhSW+k9P45xow9Mer/Mi/t8wBVow1359AE+Jab3GK5GOCSJGRU8\nyNSIeDKaZDgb/Pk2TLe7Ivkb5ahhIPG4cDU5Il5OjZbbOtCxa+KUaJGFBhm+alb+\nDL33Hk+A+agYOwvMIA==\n-----END CERTIFICATE-----'
    pem_data = sys.argv[1] if len(sys.argv) > 1 else PEM_DATA
    pprint(certificate_info(pem_data))
