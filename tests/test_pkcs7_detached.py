# vim: set tabstop=4 shiftwidth=4 expandtab:

import pytest
import mock
import os
import sys
import re
import subprocess

from pkcs7_vectors import SAMPLE_VALID_IDENTITY_DOC
from pkcs7_vectors import SAMPLE_VALID_IDENTITY_SIGNATURE
from pkcs7_vectors import SAMPLE_VALID_AWS_CERT
from pkcs7_vectors import SAMPLE_BOGUS_IDENTITY_DOC
from pkcs7_vectors import SAMPLE_BOGUS_IDENTITY_SIGNATURE
from pkcs7_vectors import SAMPLE_BOGUS_AWS_CERT
from pkcs7_vectors import SAMPLE_INVALID_IDENTITY_SIGNATURE
from pkcs7_vectors import SAMPLE_INVALID_AWS_CERT
from pkcs7_vectors import SAMPLE2_VALID_IDENTITY_DOC
from pkcs7_vectors import SAMPLE2_VALID_IDENTITY_SIGNATURE

import pkcs7_detached
from pkcs7_detached import aws_certificates

def test_verify_valid():
    document = SAMPLE_VALID_IDENTITY_DOC
    signature = SAMPLE_VALID_IDENTITY_SIGNATURE
    certificate = SAMPLE_VALID_AWS_CERT

    r = pkcs7_detached.verify_detached_signature(document, signature, certificate)
    assert r == True

def test_verify_bogus_doc():
    document = SAMPLE_BOGUS_IDENTITY_DOC
    signature = SAMPLE_VALID_IDENTITY_SIGNATURE
    certificate = SAMPLE_VALID_AWS_CERT

    r = pkcs7_detached.verify_detached_signature(document, signature, certificate)
    assert r == False

def test_verify_bogus_signature():
    document = SAMPLE_VALID_IDENTITY_DOC
    signature = SAMPLE_BOGUS_IDENTITY_SIGNATURE
    certificate = SAMPLE_VALID_AWS_CERT

    r = pkcs7_detached.verify_detached_signature(document, signature, certificate)
    assert r == False

def test_verify_bogus_certificate():
    document = SAMPLE_VALID_IDENTITY_DOC
    signature = SAMPLE_VALID_IDENTITY_SIGNATURE
    certificate = SAMPLE_BOGUS_AWS_CERT

    r = pkcs7_detached.verify_detached_signature(document, signature, certificate)
    assert r == False

def test_verify_valid_aws():
    r = pkcs7_detached.verify_detached_signature(SAMPLE2_VALID_IDENTITY_DOC, SAMPLE2_VALID_IDENTITY_SIGNATURE, aws_certificates.PUBLIC_REGIONS)
    assert r == True
