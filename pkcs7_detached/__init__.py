# vim: set tabstop=4 shiftwidth=4 expandtab:

import logging

from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.bindings._openssl import ffi, lib

"""
Use the Cryprography hazmat backend (OpenSSL binding) to verify
a detached PKCS7 signarure.

Base on the steps in https://github.com/openssl/openssl/blob/master/apps/smime.c

certificate is a PEM formated X509 certificate

"""


def verify_detached_signature(document, signature, certificate):
    logger = logging.getLogger(__name__)

    logger.debug(
        "verify_detached_signature('{}', '{}', '{}')".format(
            document, signature, certificate
        )
    )

    try:
        # Format the signature into PKCS7 PEM format
        pkcs7 = signature.split("\n")

        # Remove blank training lines
        while pkcs7[-1] == "":
            pkcs7.pop()

        # Add armour if missing
        if not pkcs7[0] == "-----BEGIN PKCS7-----":
            pkcs7.insert(0, "-----BEGIN PKCS7-----")
            pkcs7.append("-----END PKCS7-----")

        pkcs7 = "\n".join(pkcs7)

        logger.debug(pkcs7)

        # Load the string into a bio
        bio = backend._bytes_to_bio(pkcs7.encode())

        # Create the pkcs7 object
        p7 = lib.PEM_read_bio_PKCS7(bio.bio, ffi.NULL, ffi.NULL, ffi.NULL)

        # Load the specified certificate
        other_cert = backend.load_pem_x509_certificate(certificate.encode())
        stack = lib.sk_X509_new_null()
        lib.sk_X509_push(stack, other_cert._x509)

        # We need a CA store, even though we don't use it
        store = lib.X509_STORE_new()

        # Load the document into a bio
        content = backend._bytes_to_bio(document.encode("utf-8"))

        # Flags
        flags = lib.PKCS7_NOVERIFY

        # https://www.openssl.org/docs/man1.0.2/crypto/PKCS7_verify.html
        if lib.PKCS7_verify(p7, stack, store, content.bio, ffi.NULL, flags) == 1:
            return True
    except Exception as e:
        logger.error("verify_detached_signature exception={}".format(str(e)))
        return False
    return False
