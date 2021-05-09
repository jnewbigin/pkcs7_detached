#!/usr/bin/env bash
set -euo pipefail

# This script runs from CI to update the requirements for this version of python
# and created a branch/PR for the update


BRANCH="$(python3 -c 'import sys; import time; print(f"requriements-{sys.version_info.major}-{sys.version_info.minor}-{time.time():.0f}")')"

git config --global user.name 'GitHub Actions'
git config --global user.email 'john.newbigin@chrysocome.net'
git remote set-url origin https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}
	            
git checkout -b "$BRANCH"
scripts/requirements.sh
git add requirements/*.txt
git commit -m "Auto-update requirements"
git push
