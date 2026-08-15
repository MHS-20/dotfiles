#!/usr/bin/env bash

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <wifi-name> <password>"
  exit 1
fi

SSID="$1"
PASSWORD="$2"

nmcli device wifi connect "$SSID" password "$PASSWORD"
