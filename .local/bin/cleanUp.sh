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
# 8. mise: unused tool versions
# =========================
echo " Pruning unused mise versions..."
mise prune -y 2>/dev/null || true

# =========================
# 9. Rust: old toolchains (keep newest)
# =========================
if command -v rustup >/dev/null; then
  echo " Removing old Rust toolchains..."
  old=$(rustup toolchain list | awk '{print $1}' | sort -V | head -n -1)
  [ -n "$old" ] && rustup toolchain uninstall $old || true
fi
rm -rf ~/.cargo/registry/cache ~/.cargo/registry/src 2>/dev/null || true

# =========================
# 10. Go module cache
# =========================
echo " Cleaning Go module cache..."
command -v go >/dev/null && go clean -modcache || true

# =========================
# 11. Discord cache (only if not running)
# =========================
if ! pgrep -x -i discord >/dev/null; then
  echo " Cleaning Discord cache..."
  rm -rf ~/.config/discord/{Cache,"Code Cache",GPUCache} 2>/dev/null || true
else
  echo " Discord running, skipping its cache"
fi

# =========================
# 12. Browser / app caches (only if app not running)
# =========================
clean_if_closed() { # $1 = process name, rest = paths
  local proc=$1; shift
  if pgrep -i -f "$proc" >/dev/null; then
    echo " $proc running, skipping its cache"
  else
    echo " Cleaning $proc cache..."
    rm -rf "$@" 2>/dev/null || true
  fi
}
BRAVE="$HOME/.config/BraveSoftware/Brave-Browser"
clean_if_closed brave \
  "$BRAVE"/*/"Service Worker"/CacheStorage "$BRAVE"/*/{Cache,"Code Cache",GPUCache} \
  "$BRAVE"/{component_crx_cache,extensions_crx_cache,GrShaderCache,ShaderCache,GPUPersistentCache}
clean_if_closed Telegram ~/.local/share/TelegramDesktop/tdata/user_data*
clean_if_closed Z-Library ~/.config/Z-Library/Cache

# =========================
# 13. Dev tool caches
# =========================
echo " Cleaning dev tool caches..."
command -v npm >/dev/null && npm cache clean --force 2>/dev/null || true
rm -rf ~/.local/share/vcpkg/{buildtrees,downloads,packages} 2>/dev/null || true
: > ~/.local/state/nvim/lsp.log 2>/dev/null || true

# =========================
# Done
# =========================
echo " Cleanup finished!"
echo " Disk usage summary:"
df -h /
