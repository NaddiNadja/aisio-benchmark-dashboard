#! /bin/bash

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
source $SRC/util.sh

printcmd "tree"

tree | head -n 500 | while read -r line ; do printf '%s\n' "$line"; sleep 0.05; done

sleep 2
echo "^C"

touch $TMP_FILE