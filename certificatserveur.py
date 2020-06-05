# -*- coding: utf-8 -*-
"""
Created on Sun May 10 23:21:37 2020

@author: Mr ABBAS-TURKI
"""

from PKI_utile import sign_csr
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from getpass import getpass


csr_file = open("serveur-csr.pem", "rb")
csr = x509.load_pem_x509_csr(csr_file.read(), default_backend())
print(csr)

ca_public_key_file = open("ca-cle-publique.pem", "rb")
ca_public_key = x509.load_pem_x509_certificate(
    ca_public_key_file.read(), 
    default_backend()
    )
print(ca_public_key)


ca_private_key_file = open("ca-cle-privee.pem", "rb")
ca_private_key = serialization.load_pem_private_key(
    ca_private_key_file.read(),
    getpass().encode("utf-8"),
    default_backend(),
    )

sign_csr(csr, ca_public_key, ca_private_key, "serveur-cle-publique.pem")