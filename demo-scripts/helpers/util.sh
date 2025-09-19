#! /bin/bash

TMP_FILE="/tmp/pane_done"
ZELLIJ_ARGS="action new-pane --floating --width 77% --height 77% -x 1 -y 25% --close-on-exit"
TRAINING_DATA="/mnt/two/train"


typeout () {
  local text="$1"
  for ((i=0; i<${#text}; i++)); do
    echo -n "${text:$i:1}"
    sleep_time=$(awk -v min=0.05 -v max=0.1 'BEGIN{srand(); print min+rand()*(max-min)}')
    sleep "$sleep_time"
  done
  echo
}

printcmd () {
  sleep 2
  local cmd="$1"
  typeout "[1;35m\$[0m [1;34m${cmd}[0m"
}

printandeval () {
  local cmd="$1"
  printcmd $cmd
  eval "$cmd"
  echo
}

printlines () {
  local lines=("$@")
  local len=${#lines[0]}
  
  tput sc  

  for ((i=0; i<len; i++)); do
    tput rc  
    for line in "${lines[@]}"; do
      echo "${line:0:i+1}"
    done
    sleep 0.05
  done
}

run_zellij() {
  local name="$1"
  local script="$2"
  zellij $ZELLIJ_ARGS --name "$name" -- "$script"
  while [ ! -f "$TMP_FILE" ]; do sleep 0.1; done
  rm "$TMP_FILE"
}
