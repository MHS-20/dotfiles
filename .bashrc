	#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias ll='ls -l --color=auto'
alias k='kubectl'
alias tf='terraform'
alias zippa='zip -r "$(basename "$PWD").zip" .'
alias dotfiles='git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'

#PS1='[\u@\h \W]\$ '
PS1='\[\e[0;32m\]\u@\h \[\e[0;34m\]\w \$\[\e[0m\] '

if [ -f /etc/profile.d/vte.sh ]; then
    source /etc/profile.d/vte.sh
fi

export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/sentinel/bin:$PATH"

### SSH AGENT
eval $(keychain --eval --quiet ~/.ssh/id_ed25519)
# if [ -z "$SSH_AUTH_SOCK" ]; then
#    eval "$(ssh-agent -s)"
# fi
# ssh-add ~/.ssh/id_ed25519

### RUST
source $HOME/.cargo/env

### NODE
export NVM_DIR="$HOME/.config/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

### PYTHON
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

### JAVA
export JAVA_HOME="$HOME/.sdkman/candidates/java/current"
export PATH="$JAVA_HOME/bin:$PATH"

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"

