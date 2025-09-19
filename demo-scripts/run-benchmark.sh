#! /bin/bash

SRC="/root/git/ocp-demo/misc"
DASHBOARD_IP=""
BACKEND=$1

python3 -m venv $SRC/.venv
$SRC/.venv/bin/pip install -r $SRC/requirements.txt

clear
$SRC/.venv/bin/python3 ~/git/ocp-demo/misc/run-benchmark.py $BACKEND -d $DASHBOARD_IP