#!/bin/sh
# Build the multi-stage Docker image. Usage: ./scripts/docker-build.sh [tag]
# Default tag: commit-guardian-ci:latest. Requires Docker (not installed on
# this VM — builds are verified in GitHub Actions CI).
set -e
cd "$(dirname "$0")/.."
TAG="${1:-commit-guardian-ci:latest}"
docker build -t "$TAG" .
echo "Built $TAG"
