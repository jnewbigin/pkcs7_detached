import requests
from pkcs7_detached import verify_detached_signature, aws_certificates
import json
from pprint import pprint


def main():
    print("Verifying ec2 instance identity document")

    r = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document")
    identity_document = r.text

    r = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/pkcs7")
    pkcs7 = r.text

    if verify_detached_signature(
        identity_document, pkcs7, aws_certificates.PUBLIC_REGIONS
    ):
        print("Verified")
        identity = json.loads(identity_document)
        pprint(identity)
    else:
        print("Identity is not valid")


if __name__ == "__main__":
    main()
