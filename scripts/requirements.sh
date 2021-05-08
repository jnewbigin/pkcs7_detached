#!/usr/bin/env bash
set -euo pipefail

PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
echo "Building requirements for python $PYTHON_VERSION" >&2

python3 -m pip install pip-tools --user --upgrade
python3 -m piptools compile \
	--allow-unsafe \
	--upgrade requirements/prod.in \
	--output-file "requirements/prod-${PYTHON_VERSION}.txt"
python3 -m piptools compile \
	--allow-unsafe \
	--upgrade requirements/dev.in \
	--output-file "requirements/dev-${PYTHON_VERSION}.txt"
