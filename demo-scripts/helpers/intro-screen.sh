#! /bin/bash

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
source $SRC/util.sh

clear

echo
echo
echo
echo
echo
echo

lines=(
"[1;31m                                       ▄▄        ██       ▄▄▄▄     ▄▄▄▄▄▄     ▄▄▄▄   [0m"
"[0;32m                                      ████       ▀▀     ▄█▀▀▀▀█    ▀▀██▀▀    ██▀▀██  [0m"
"[1;32m                                      ████     ████     ██▄          ██     ██    ██ [0m"
"[0;33m                                     ██  ██      ██      ▀████▄      ██     ██    ██ [0m"
"[1;33m                                     ██████      ██          ▀██     ██     ██    ██ [0m"
"[0;34m                                    ▄██  ██▄  ▄▄▄██▄▄▄  █▄▄▄▄▄█▀   ▄▄██▄▄    ██▄▄██  [0m"
"[1;34m                                    ▀▀    ▀▀  ▀▀▀▀▀▀▀▀   ▀▀▀▀▀     ▀▀▀▀▀▀     ▀▀▀▀   [0m"
)
printlines "${lines[@]}".

echo
echo "                                            [1;35mAccelerator-initiated Storage I/O[0m"

sleep 5