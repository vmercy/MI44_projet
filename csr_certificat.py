# -*- coding: utf-8 -*-
"""
Created on Mon May 11 07:06:46 2020

@author: Mr ABBAS-TURKI
"""


from PKI_utile import generate_csr, generate_private_key
private_key = generate_private_key("serveur-cle-privee.pem","valentinmercy")
csr = generate_csr(private_key,"serveur-csr.pem",country="FR",state="AL",locality="Mulhouse",org="UTBM",hostname="moncsr.com")