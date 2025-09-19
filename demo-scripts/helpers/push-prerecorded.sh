#! /bin/bash

DASHBOARD_IP=""
echo "Running benchmarks ..."
echo "press Ctrl+C to cancel"
python3 ~/git/ocp-demo/misc/push.py -d $DASHBOARD_IP

touch /tmp/demo_done
sleep 10