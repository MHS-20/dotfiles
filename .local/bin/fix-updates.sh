#!/usr/bin/env bash
# fix-updates.sh — Fix common pacman update problems on Arch Linux
# Run as root.

set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "ERROR: Run this script as root (sudo)." >&2
  exit 1
fi

echo "==> [1/6] Killing any stale pacman processes ..."
if pgrep -x pacman &>/dev/null; then
  killall pacman 2>/dev/null || true
fi

echo "==> [2/6] Removing pacman lock file if present ..."
[[ -f /var/lib/pacman/db.lck ]] && rm -v /var/lib/pacman/db.lck

echo "==> [3/6] Refreshing keyring ..."
pacman-key --refresh-keys
pacman-key --populate archlinux

echo "==> [4/6] Clearing package cache (keeping last 2 versions) ..."
paccache -rk2

echo "==> [5/6] Forcing a full database refresh ..."
pacman -Syy

echo "==> [6/6] Upgrading the system ..."
pacman -Su --noconfirm

echo ""
echo "==> Done! System is up to date."
echo "    If signature errors persist, run: pacman-key --init && pacman-key --populate archlinux"
