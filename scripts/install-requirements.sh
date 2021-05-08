#!/usr/bin/env bash
set -euo pipefail

PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
echo "Installing requirements for python $PYTHON_VERSION" >&2

python -m pip install -r "requirements/dev-${PYTHON_VERSION}.txt" --user

