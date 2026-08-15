#!/usr/bin/env bash
set -e
REPO_NAME=$(basename "$PWD")
gh repo create "$REPO_NAME" --source=. --remote=origin --push --public

