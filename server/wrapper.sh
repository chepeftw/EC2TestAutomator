#!/bin/bash

mkdir -p /var/log/golang

# Start the first process
$GOBIN/Gossip /treesip/conf1.yml &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start Gossip process: $status"
  exit $status
fi

# Start the second process
$GOBIN/Treesip /treesip/conf1.yml &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start Treesip1 process: $status"
  exit $status
fi

$GOBIN/Treesip /treesip/conf2.yml &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start Treesip2 process: $status"
  exit $status
fi

# Naive check runs checks once a minute to see if either of the processes exited.
# This illustrates part of the heavy lifting you need to do if you want to run
# more than one service in a container. The container will exit with an error
# if it detects that either of the processes has exited.
# Otherwise it will loop forever, waking up every 60 seconds

while /bin/true; do
  PROCESS_1_STATUS=$(ps aux |grep -q Gossip |grep -v grep)
  PROCESS_2_STATUS=$(ps aux |grep -q "Treesip /treesip/conf1.yml" |grep -v grep)
  PROCESS_3_STATUS=$(ps aux |grep -q "Treesip /treesip/conf2.yml" | grep -v grep)
  # If the greps above find anything, they will exit with 0 status
  # If they are not both 0, then something is wrong
  if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 -o $PROCESS_3_STATUS -ne 0 ]; then
    echo "One of the processes has already exited."
    exit -1
  fi
  sleep 60
done