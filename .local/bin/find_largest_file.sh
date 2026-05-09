#!/usr/bin/env bash
# find_largest_file.sh — Find the largest files on the system
# Usage: ./find_largest_file.sh [directory] [top N]

set -euo pipefail

DIR="${1:-/}"
TOP="${2:-20}"

echo "==> Searching for the $TOP largest files in: $DIR"
echo "    (this may take a moment...)"
echo

find "$DIR" -xdev -type f -printf '%s\t%p\n' 2>/dev/null \
  | sort -rn \
  | head -n "$TOP" \
  | awk 'BEGIN { OFS="\t" }
    {
      bytes = $1
      path  = $2
      if (bytes >= 1073741824)      printf "%.2f GiB\t%s\n", bytes/1073741824, path
      else if (bytes >= 1048576)    printf "%.2f MiB\t%s\n", bytes/1048576,    path
      else if (bytes >= 1024)       printf "%.2f KiB\t%s\n", bytes/1024,       path
      else                          printf "%d   B\t%s\n",   bytes,             path
    }'
