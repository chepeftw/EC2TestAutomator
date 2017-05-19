#!/bin/bash -

# Make the script to run at boot time
# chmod +x /home/ubuntu/EC2TestAutomator/main.sh
# sudo cp treesip.service /etc/systemd/system/
# chmod 664 /etc/systemd/system/treesip.service
# systemctl daemon-reload
# systemctl enable treesip.service

# To test
# systemctl start treesip.service

# First, we get the instance ID, this IP is fixed, is not dependant on anything
INSTANCE=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
# Then based on the Instance ID, we get all tags
TAGS=$(~/.local/bin/aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE" --output=text)

echo "$TAGS"

# Then we select the tag we need
TS_NODES=$(echo "$TAGS" | grep Nodes | cut -f5)
TS_CYCLES=$(echo "$TAGS" | grep Cycles | cut -f5)
TS_TIME=$(echo "$TAGS" | grep Timeemu | cut -f5)
TS_TIMEOUT=$(echo "$TAGS" | grep Timeout | cut -f5)
TS_SIZE=$(echo "$TAGS" | grep Size | cut -f5)
TS_NAME=$(echo "$TAGS" | grep EmulationName | cut -f5)
TS_SPEED=$(echo "$TAGS" | grep Speed | cut -f5)
TS_PAUSE=$(echo "$TAGS" | grep Pause | cut -f5)

echo "Nodes $TS_NODES"
echo "Cycles $TS_CYCLES"
echo "Time $TS_TIME"
echo "Timeout $TS_TIMEOUT"
echo "Size $TS_SIZE"
echo "Speed $TS_SPEED"
echo "Pause $TS_PAUSE"
echo "Name $TS_NAME"

# We make sure we got the values, otherwise we abort mission
if [ -z "$TS_NODES" ]
  then
    echo "No number of nodes supplied"
    exit 1
fi

if [ -z "$TS_TIME" ]
  then
    echo "No time supplied"
    exit 1
fi

if [ -z "$TS_CYCLES" ]
  then
    echo "No number of cycles supplied"
    exit 1
fi


if [ -z "$TS_NAME" ]
  then
    echo "No name supplied"
    exit 1
fi

if [ -z "$TS_TIMEOUT" ]
  then
    TS_TIMEOUT="200"
fi

if [ -z "$TS_SIZE" ]
  then
    TS_SIZE="300"
fi

if [ -z "$TS_SPEED" ]
  then
    TS_SPEED="5"
fi

if [ -z "$TS_PAUSE" ]
  then
    TS_PAUSE="1"
fi


# We make sure we got the values, otherwise we abort mission
COUNTER=0

cd /home/ubuntu/tap
rm -rf var/archive/

date > /home/ubuntu/foo.txt

export NS3_HOME=/home/ubuntu/workspace/source/ns-3.26
while [  $COUNTER -lt $TS_CYCLES ]; do

    cd /home/ubuntu/tap
	DATENOW=$(date +"%y_%m_%d_%H_%M")
	mkdir -p var/archive/$DATENOW
	mv var/log/* var/archive/$DATENOW/

	echo "python3 main.py -n $TS_NODES -t $TS_TIME -to $TS_TIMEOUT -s $TS_SIZE full"
	python3 main.py -n $TS_NODES -t $TS_TIME -to $TS_TIMEOUT -s $TS_SIZE -ns $TS_SPEED -np $TS_PAUSE -c $COUNTER full

	cd /home/ubuntu/EC2TestAutomator
	echo "python3 statscollector2.py -ns $TS_SPEED -np $TS_PAUSE $TS_NAME $TS_NODES $TS_TIME $TS_TIMEOUT $TS_SIZE"
	python3 statscollector2.py $TS_NAME $TS_NODES $TS_TIME $TS_TIMEOUT $TS_SIZE

	let COUNTER=COUNTER+1
	echo $COUNTER >> /home/ubuntu/foo.txt
done

date >> /home/ubuntu/foo.txt
echo $TS_NODES >> /home/ubuntu/foo.txt
echo $TS_TIME >> /home/ubuntu/foo.txt
echo $TS_CYCLES >> /home/ubuntu/foo.txt
echo "Done!" >> /home/ubuntu/foo.txt

sleep 5m

if [ ! -f /home/ubuntu/continue.txt ]; then
    sudo poweroff
fi