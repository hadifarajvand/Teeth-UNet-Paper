#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Downloads/prepares datasets directly under this repository's data/ directory.
# Optional arguments are forwarded, for example:
#   ./download_datasets.sh --dataset tdd
#   ./download_datasets.sh --dataset all
#   ./download_datasets.sh --dataset tdd --archive /path/to/tdd.zip
python scripts/download_datasets.py "$@"
