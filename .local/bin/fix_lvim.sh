#!/bin/bash

# --- LunarVim Repair & Update Script ---
# Designed for Arch Linux users experiencing Treesitter/Plugin errors.

echo "🚀 Starting LunarVim Repair..."

# 1. Clear Treesitter Parsers and Cache
# These are the most common causes of 'nil value' and 'Query error' messages.
echo "🧹 Clearing Treesitter cache and compiled parsers..."
rm -rf ~/.local/share/lunarvim/site/pack/lazy/opt/nvim-treesitter/parser/*
rm -rf ~/.cache/nvim/treesitter
rm -rf ~/.local/share/nvim/treesitter # Just in case standard nvim paths are used

# 2. Clear Plugin State
# This forces Lazy.nvim to re-calculate the plugin graph on next launch.
echo "🧹 Clearing plugin state..."
rm -rf ~/.local/share/lunarvim/lazy/lazy.nvim

# 3. Update System Dependencies (Arch specific)
# Ensures Neovim and the tools LunarVim relies on are current.
echo "📦 Updating system dependencies via pacman..."
sudo pacman -S --needed --noconfirm neovim ripgrep fd git make nodejs npm python-pip

# 4. Trigger Internal Updates
# We run these via the lvim CLI so you don't have to fight the UI errors.
echo "🔄 Updating LunarVim Core..."
lvim +LvimUpdate +q

echo "🔄 Updating Plugins (Lazy)..."
lvim +Lazy! sync +q

echo "🔄 Reinstalling Treesitter Parsers..."
# Reinstalling 'lua', 'vim', and 'help' as they are core to lvim functioning.
lvim +TSUpdate +q

# 5. Fix Mason (LSPs and Formatters)
# Sometimes the binaries in Mason become incompatible with new Arch libs.
echo "🛠️ Checking Mason packages..."
# This doesn't delete them, but ensures Mason is ready to reinstall if needed.
# Launching lvim once normally is usually enough for Mason to settle.

echo "------------------------------------------------"
echo "✅ Repair Attempt Complete!"
echo "------------------------------------------------"
echo "Next Steps:"
echo "1. Open lvim. If you still see errors, run ':Lazy clean' followed by ':Lazy sync'."
echo "2. Run ':LvimInfo' to check for any missing system requirements."
echo "3. If errors persist, consider a full reinstall as the config structure may have changed."
