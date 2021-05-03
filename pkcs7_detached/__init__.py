# vim: set tabstop=4 shiftwidth=4 expandtab:


"""
Use the Cryprography hazmat backend (OpenSSL binding) to verify
a detached PKCS7 signarure.

Base on the steps in https://github.com/openssl/openssl/blob/master/apps/smime.c

certificate is a PEM formated X509 certificate
"""

import logging

from cryptography.hazmat.backends.openssl.backend import backend # type: ignore
from cryptography.hazmat.bindings._openssl import ffi, lib # type: ignore # pylint: disable=E0611

class ValidationError(Exception):
    """Represent an error in the PKCS7 detached signature validation"""

def __ascii_armor(payload: str, header: str) -> str:
    """Add ascii armour for the specified header type to an ascii payload
    Will not add if the correct header is already present
    Will remove any trailing newlines
    """
    try:
        begin = "-----BEGIN {}-----".format(header)
        end = "-----END {}-----".format(header)

        lines = payload.split("\n")

        # Remove blank training lines
        while lines[-1] == "":
            lines.pop()

        # Add armour if missing
        if not lines[0] == begin:
            lines.insert(0, begin)
            lines.append(end)

        return "\n".join(lines)
    except IndexError:
        raise ValidationError(f"Unable to ascii armor {header}") from None


def verify_detached_signature(document: str, signature: str, certificate: str) -> bool:
    """Verify a detached signature
    Parameters
    ----------
    document : str
        The document to be verified
    signature : str
        The signature to verify. The signature may inculde the PKCS7 ascii armor
    certificate : str
        The certificate of the signer. The certificate must include the CERTIFICATE ascii armor
    """
    logger = logging.getLogger(__name__)

    logger.debug(
        "verify_detached_signature('%s', '%s', '%s')", document, signature, certificate
    )

    try:
        pkcs7 = __ascii_armor(signature, "PKCS7")
        logger.debug(pkcs7)

        # Load the string into a bio
        bio = backend._bytes_to_bio(pkcs7.encode()) # pylint: disable=W0212

        # Create the pkcs7 object
        pkcs7_object = lib.PEM_read_bio_PKCS7(bio.bio, ffi.NULL, ffi.NULL, ffi.NULL)

        # Load the specified certificate
        certificate = __ascii_armor(certificate, 'CERTIFICATE')
        other_cert = backend.load_pem_x509_certificate(certificate.encode())
        stack = lib.sk_X509_new_null()
        lib.sk_X509_push(stack, other_cert._x509) # pylint: disable=W0212

        # We need a CA store, even though we don't use it
        store = lib.X509_STORE_new()

        # Load the document into a bio
        content = backend._bytes_to_bio(document.encode("utf-8")) # pylint: disable=W0212

        # Flags
        flags = lib.PKCS7_NOVERIFY

        # https://www.openssl.org/docs/man1.0.2/crypto/PKCS7_verify.html
        if lib.PKCS7_verify(pkcs7_object, stack, store, content.bio, ffi.NULL, flags) == 1:
            return True
    except ValidationError as error:
        logger.error("verify_detached_signature exception=%s", str(error))
        return False
    return False
