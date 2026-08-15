#!/usr/bin/env bash

nmcli device wifi rescan >/dev/null 2>&1
sleep 1

nmcli --fields IN-USE,SSID,SIGNAL,SECURITY device wifi list
