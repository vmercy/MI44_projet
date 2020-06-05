# -*- coding: utf-8 -*-
"""
Created on Thu May 14 15:59:55 2020

@author: Mr ABBAS-TURKI
"""

import sys
import os
import ssl
import pprint

def main():
    #les lignes [17-20] remplacent leurs equivalents Windows car je suis sous Linux
    cert_file_base_name = sys.argv[1]
    cert_file_name = os.path.realpath(__file__).split("/")
    cert_file_name = "/".join(cert_file_name[:-1])+"/"+cert_file_base_name
    print(cert_file_name)
    try:
        cert_dict = ssl._ssl._test_decode_cert(cert_file_name)
    except Exception as e:
        print("Error decoding certificate: {0:}".format(e))
    else:
        print("Certificate ({0:s}) data:\n".format(cert_file_base_name))
        pprint.pprint(cert_dict)

if __name__ == "__main__":
    print("Python {0:s} {1:d}bit on {2:s}\n".format(" ".join(item.strip() for item in sys.version.split("\n")), 64 if sys.maxsize > 0x100000000 else 32, sys.platform))
    main()
    print("\nDone.")