#
# ~/.bash_profile
#

[[ -f ~/.bashrc ]] && . ~/.bashrc
. "$HOME/.cargo/env"

eval $(keychain --eval --quiet ~/.ssh/id_ed25519)
