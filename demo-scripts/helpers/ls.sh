#! /bin/bash

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
source $SRC/util.sh

printcmd "ls -lh n03447721"

res1=$(ls -lh n03447721 | head -n 10)
res2=$(ls -lh n03447721 | tail -n 10)

echo "$res1"
echo "     [...]"
echo "$res2"

sleep 4
touch $TMP_FILE