# -*- coding: utf-8 -*-
"""
Created on Sun May 10 17:08:59 2020

@author: Mr ABBAS-TURKI
"""
#**********************génération des clés**********************************
# les lignes de 9 à 11 importent les librairies requises pour générer les clés
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

#fonction de génération de la clé privée
def generate_private_key(nomfichier: str, motdepasse: str): 
    # les lignes 16 à 18 génèrent la clé privée. 65537 est l'exposant public magic 
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    #les lignes 20 à 21 fixent les paramètres d'encodage pour le chiffrement de la clé privée
    utf8_pass = motdepasse.encode("utf-8")
    algorithm = serialization.BestAvailableEncryption(utf8_pass)
    #les lignes 23 à 31 crée le fichier "nomfichier" contenant le clés privés (p,q,n) chiffré avec le motdepasse 
    with open(nomfichier, "wb") as keyfile:
        keyfile.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=algorithm,
            )
        )
    return private_key
#********************devenir sa propre autorité de certification*************
# les lignes de 34 à 37 importent les librairies requises pour la création du certificat de l'autorité de certification
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
def generate_public_key(private_key, nomdefichier, **kwargs):
    # les lignes 39 à 50 construisent les information qui font l'objet de la certification
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, kwargs["country"]),
            x509.NameAttribute(
                NameOID.STATE_OR_PROVINCE_NAME, kwargs["state"]
            ),
            x509.NameAttribute(NameOID.LOCALITY_NAME, kwargs["locality"]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, kwargs["org"]),
            x509.NameAttribute(NameOID.COMMON_NAME, kwargs["hostname"]),
        ]
    )

    # Parce que ce certificat est auto-signé
    issuer = subject

    # Les lignes 56 et 57 donne la durée de validité de la clé publique (60 jours)
    valid_from = datetime.utcnow()
    valid_to = valid_from + timedelta(days=60)

    # Les lignes de 60 à 68 ajourtent toutes les informations au constructeur de la clé publique pour que l'ensemble soit signé 
    builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(valid_from)
        .not_valid_after(valid_to)
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True,)
    )

    # Les lignes 71 à 73 signent le certificat avec la clé privée
    public_key = builder.sign(
        private_key, hashes.SHA256(), default_backend()
    )
    # Les lignes de 75 à 78 écrivent le cerficat dans le fichier "nomdefichier"
    with open(nomdefichier, "wb") as certfile:
        certfile.write(public_key.public_bytes(serialization.Encoding.PEM))

    return public_key
#générer le fichier de requête de certiication
def generate_csr(private_key, nomdefichier, **kwargs):
    # les lignes 82 à 92 construisent les information qui font l'objet de la certification
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, kwargs["country"]),
            x509.NameAttribute(
                NameOID.STATE_OR_PROVINCE_NAME, kwargs["state"]
            ),
            x509.NameAttribute(NameOID.LOCALITY_NAME, kwargs["locality"]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, kwargs["org"]),
            x509.NameAttribute(NameOID.COMMON_NAME, kwargs["hostname"]),
        ]
    )

    # de 95 à 98 génère les alternatives de serveurs DNS valides pour le certificat
    alt_names = []
    for name in kwargs.get("alt_names", []):
        alt_names.append(x509.DNSName(name))
    san = x509.SubjectAlternativeName(alt_names)
    # de 100 à 104 génerent les différents constructeur d'objet des attributs du CSR 
    builder = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(subject)
        .add_extension(san, critical=False)
    )
    # La ligne suivante signe le CSR avec la clé privé 
    csr = builder.sign(private_key, hashes.SHA256(), default_backend())
    # les 108 et 109 ecrivent la requete de signature du certificat dans le fichier PEM 
    with open(nomdefichier, "wb") as csrfile:
        csrfile.write(csr.public_bytes(serialization.Encoding.PEM))

    return csr

#creer une cle publique signee par le CA
def sign_csr(csr, ca_cle_publique, ca_cle_privee, nomdefichier):
    #les lignes 116 et 117 definissent la validite du certificat qui sera genere à 60 jours 
    valid_from = datetime.utcnow()
    valid_until = valid_from + timedelta(days=60)
# les 119 à 127 donnes les attributs du certificat    
    builder = (
        x509.CertificateBuilder()
        .subject_name(csr.subject) #l'objet est bien celui du CSR
        .issuer_name(ca_cle_publique.subject) #issuer est le CA
        .public_key(csr.public_key()) #obtient la clé publique du CSR.
        .serial_number(x509.random_serial_number())
        .not_valid_before(valid_from)
        .not_valid_after(valid_until)
    )
#les lignes 129 et 130 ajoute les extentions existantes dans le certificat csr
    for extension in csr.extensions:
        builder = builder.add_extension(extension.value, extension.critical)
#les lignes de 132 à 136 signent la clé publique avec la clé privée du CA
    public_key = builder.sign(
        private_key=ca_cle_privee,
        algorithm=hashes.SHA256(),
        backend=default_backend(),
    )
#les lignes 138 et 139 génèrent le cerficat signée par le CA
    with open(nomdefichier, "wb") as keyfile:
        keyfile.write(public_key.public_bytes(serialization.Encoding.PEM))






