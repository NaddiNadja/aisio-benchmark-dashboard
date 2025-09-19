#! /bin/bash

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
source $SRC/util.sh

printcmd "du -h --max-depth=1"

res1=$(du -h --max-depth=1 | head -n 10)
res2=$(du -h --max-depth=1 | tail -n 10)

echo "$res1"
echo "     [...]"
echo "$res2"

sleep 3
touch $TMP_FILE