#!/bin/bash

docker run -i --rm python:3.6 bash << END
python3 -m pip install cryptography==2.3
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pkcs7_detached
python3 << EOF
import pkcs7_detached
print('Package works')
EOF
END

