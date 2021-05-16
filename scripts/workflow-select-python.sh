#!/usr/bin/env bash
set -euo pipefail

echo "Looking for python version on ${GITHUB_REF:-}"
ALL_VERSIONS="3.6, 3.7, 3.8, 3.9"

BRANCH="${GITHUB_REF##*/}"

if [[ $BRANCH =~ requriements-([0-9]+)-([0-9]+) ]] ; then
	echo "Branch $BRANCH is python version ${BASH_REMATCH}" >&2
	VERSION="${BASH_REMATCH[1]}.${BASH_REMATCH[2]}"
else
	VERSION="$ALL_VERSIONS"
fi

echo "::set-output name=python-versions::[$VERSION]"
