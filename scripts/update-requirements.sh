#!/usr/bin/env bash
set -euo pipefail

# This script runs from CI to update the requirements for this version of python
# and created a branch/PR for the update

PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
BRANCH="$(python3 -c 'import sys; import time; print(f"requriements-{sys.version_info.major}-{sys.version_info.minor}-{time.time():.0f}")')"

git config --global user.name 'GitHub Actions'
git config --global user.email 'john.newbigin@chrysocome.net'
git remote set-url origin https://x-access-token:${GITHUB_TOKEN}@github.com/${REPOSITORY}
	            
git checkout -b "$BRANCH"
scripts/requirements.sh
git add requirements/*.txt
git commit -m "Auto-update requirements"
git push --set-upstream origin "$BRANCH"
curl -d "{\"title\":\"Auto-update requirements for $PYTHON_VERSION\",\"base\":\"master\", \"head\":\"$BRANCH\"}" https://x-access-token:${GITHUB_TOKEN}@api.github.com/repos/${REPOSITORY}/pulls
