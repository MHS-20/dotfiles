# Omarchy environment (OMARCHY_PATH + PATH), needed even for non-interactive shells
[[ -r /usr/share/omarchy/default/bash/env-bootstrap ]] && source /usr/share/omarchy/default/bash/env-bootstrap

# If not running interactively, don't do anything else (leave this above the rc source)
[[ $- != *i* ]] && return

# All the default Omarchy aliases and functions
# (don't mess with these directly, just overwrite them here!)
source "$OMARCHY_PATH/default/bash/rc"

# Add your own exports, aliases, and functions here.
#
# Make an alias for invoking commands you use constantly
# alias p='python'

#
# ~/.bashrc
#

alias grep='grep --color=auto'
alias ll='ls -la --color=auto'
alias k='kubectl'
alias tf='terraform'
alias cat='bat'
alias agy='agy --dangerously-skip-permissions'

# alias zippa='zip -r "$(basename "$PWD").zip" .'
alias zippa='zip -r "$(basename "$PWD").zip" . -x "*.git*" "*.jar"'
alias dotfiles='git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
alias dotfiles-add='git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME add -u'

#PS1='[\u@\h \W]\$ '
PS1='\[\e[38;2;77;255;170m\]\u@\h \[\e[0;34m\]\w \$\[\e[0m\] '

if [ -f /etc/profile.d/vte.sh ]; then
  source /etc/profile.d/vte.sh
fi

export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/sentinel/bin:$PATH"
export GOPATH="$HOME/Programs/go"
export PATH="$PATH:$HOME/Programs/go/bin"

### SSH AGENT
eval $(keychain --eval --quiet ~/.ssh/id_ed25519)

# Java, Python, Node, Go, and Rust are managed by mise (~/.config/mise/config.toml);
# its shims are already on PATH via Omarchy's env-bootstrap, no setup needed here.

export VCPKG_ROOT=$HOME/.local/share/vcpkg
export PATH=$VCPKG_ROOT:$PATH
