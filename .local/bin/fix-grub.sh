#!/usr/bin/env bash
# fix-grub.sh — Reinstall and regenerate GRUB bootloader on Arch Linux
# Run as root. Works for both BIOS and UEFI systems.

set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "ERROR: This script must be run as root (use sudo)." >&2
  exit 1
fi

# ── Detect boot mode ──────────────────────────────────────────────────────────
if [[ -d /sys/firmware/efi/efivars ]]; then
  BOOT_MODE="uefi"
else
  BOOT_MODE="bios"
fi
echo "==> Detected boot mode: $BOOT_MODE"

# ── UEFI ─────────────────────────────────────────────────────────────────────
if [[ "$BOOT_MODE" == "uefi" ]]; then
  EFI_DIR="${EFI_DIR:-/boot/efi}"
  if ! mountpoint -q "$EFI_DIR"; then
    echo "ERROR: EFI partition does not appear to be mounted at $EFI_DIR." >&2
    echo "       Mount it first or set EFI_DIR to the correct path." >&2
    exit 1
  fi

  echo "==> Installing GRUB for UEFI to $EFI_DIR ..."
  grub-install \
    --target=x86_64-efi \
    --efi-directory="$EFI_DIR" \
    --bootloader-id=GRUB \
    --recheck

# ── BIOS/MBR ─────────────────────────────────────────────────────────────────
else
  # Auto-detect the disk that holds the root partition
  ROOT_DEV="$(findmnt -n -o SOURCE /)"
  DISK="$(lsblk -no PKNAME "$ROOT_DEV")"
  DISK="/dev/${DISK}"

  echo "==> Installing GRUB for BIOS to $DISK ..."
  grub-install \
    --target=i386-pc \
    --recheck \
    "$DISK"
fi

# ── Regenerate config ─────────────────────────────────────────────────────────
echo "==> Generating /boot/grub/grub.cfg ..."
grub-mkconfig -o /boot/grub/grub.cfg

echo ""
echo "==> Done! GRUB has been reinstalled and the config regenerated."
echo "    Reboot to verify."
