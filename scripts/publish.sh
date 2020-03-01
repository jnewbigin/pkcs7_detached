#!/bin/bash

# Once all is working, run:
# $ scripts/publish.sh upload.pypi.org

rm -f dist/*
python3 setup.py sdist bdist_wheel

SERVER="${1:-test.pypi.org}"
python3 -m twine upload --repository-url "https://$SERVER/legacy/" dist/*
