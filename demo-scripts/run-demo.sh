#! /bin/bash

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
source $SRC/util.sh


cleanup() {
    [ -f "$TMP_FILE" ] && rm $TMP_FILE
}
trap cleanup EXIT SIGINT


# Screen 1
$SRC/intro-screen.sh

clear

# Screen 2
typeout "The training data is located in [1;31m1000[0m directories of varying sizes."

run_zellij "Training data directories" "$SRC/du.sh"

echo
printandeval "clear"


# Screen 3
sleep 1
typeout "The data set consists of JPEG images, and their sizes range from [1;31m0.5 KiB[0m to [1;31m15368 KiB[0m."
typeout "Most files are quite small - the average file size is around [1;31m112 KiB[0m."
sleep 1
typeout "Let's take a look at some of them ..."

run_zellij "Files in the data set" "$SRC/ls.sh"

echo
printandeval "clear"


# Screen 4
sleep 1

typeout "The file system is live."
typeout "With AiSIO, the [1;31m1281167[0m files in the data set are available during I/O."

run_zellij "Data set tree" "$SRC/tree.sh"

echo
printandeval "clear"
