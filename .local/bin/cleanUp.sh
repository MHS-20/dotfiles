#!/bin/bash
set -e

echo " Arch cleanup starting..."

# =========================
# 1. Pacman cache
# =========================
echo " Cleaning pacman cache..."
sudo paccache -r || true
sudo rm -rf /var/cache/pacman/pkg/download-* 2>/dev/null || true

# =========================
# 2. Orphan packages
# =========================
echo " Removing orphan packages..."
orphans=$(pacman -Qtdq 2>/dev/null || true)
if [ -n "$orphans" ]; then
  sudo pacman -Rns $orphans
fi

# =========================
# 3. System logs
# =========================
echo " Cleaning journal logs..."
sudo journalctl --vacuum-size=100M || true

# =========================
# 4. User cache
# =========================
echo " Cleaning user cache..."
rm -rf ~/.cache/* 2>/dev/null || true

# =========================
# 5. Gradle cache (SAFE)
# =========================
echo " Cleaning Gradle cache..."
rm -rf ~/.gradle/caches 2>/dev/null || true
rm -rf ~/.gradle/daemon 2>/dev/null || true

# =========================
# 6. JetBrains cleanup
# =========================
echo " Cleaning JetBrains data..."

JETBRAINS_DIR="$HOME/.local/share/JetBrains"

if [ -d "$JETBRAINS_DIR" ]; then
  # remove old IDE versions (non-active ones)
  find "$JETBRAINS_DIR" -maxdepth 1 -type d \
    -name "IdeaIC2025*" -exec rm -rf {} + 2>/dev/null || true

  # remove Ultimate leftovers (safe if not installed)
  rm -rf "$JETBRAINS_DIR/idea-IU-"* 2>/dev/null || true

  # clean active IDE cache safely
  find "$JETBRAINS_DIR" -type d \( -name "caches" -o -name "log" -o -name "tmp" \) \
    -exec rm -rf {} + 2>/dev/null || true
fi

# =========================
# 7. Trash
# =========================
echo " Emptying trash..."
rm -rf ~/.local/share/Trash/* 2>/dev/null || true

# =========================
# Done
# =========================
echo " Cleanup finished!"
echo " Disk usage summary:"
df -h /
