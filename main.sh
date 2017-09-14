#!/usr/bin/env bash

# Redirect stdout ( > ) into a named pipe ( >() ) running "tee"
exec > >(tee -i logfile.txt)

# Without this, only stdout would be captured - i.e. your
# log file would not contain any error messages.
# SEE (and upvote) the answer by Adam Spiers, which keeps STDERR
# as a separate stream - I did not want to steal from him by simply
# adding his answer to mine.
exec 2>&1

echo "foo"
echo "bar" >&2

echo "Waiting to start ... hi :) ..."
rm -rf /home/ubuntu/continue.txt /home/ubuntu/stop.txt

if [ -z "$1" ]
  then
    echo "No argument supplied"
    sleep 2m
else
    sleep $1
fi

docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

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

echo "${TAGS}"

# Then we select the tag we need
TS_NODES=$(echo "${TAGS}" | grep Nodes | cut -f5)
TS_CYCLES=$(echo "${TAGS}" | grep Cycles | cut -f5)
TS_TIME=$(echo "${TAGS}" | grep Timeemu | cut -f5)
TS_TIMEOUT=$(echo "${TAGS}" | grep Timeout | cut -f5)
TS_SIZE=$(echo "${TAGS}" | grep Size | cut -f5)
TS_NAME=$(echo "${TAGS}" | grep EmulationName | cut -f5)
TS_SPEED=$(echo "${TAGS}" | grep Speed | cut -f5)
TS_PAUSE=$(echo "${TAGS}" | grep Pause | cut -f5)
TS_INSTANCE=$(echo "${TAGS}" | grep Instance | cut -f5)

TS_CRYPTOPIECE=$(echo "${TAGS}" | grep CryptoPiece | cut -f5)

echo "Nodes ${TS_NODES}"
echo "Cycles ${TS_CYCLES}"
echo "Time ${TS_TIME}"
echo "Timeout ${TS_TIMEOUT}"
echo "Size ${TS_SIZE}"
echo "Speed ${TS_SPEED}"
echo "Pause ${TS_PAUSE}"
echo "Name ${TS_NAME}"
echo "Instance ${TS_INSTANCE}"

echo "Crypto Piece ${TS_CRYPTOPIECE}"

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


JOBS=1

if [ "$TS_INSTANCE" == "c4.large" ]
 then
    echo "Instance is c4.large, 2 vCPU"
    JOBS=2
elif [ "$TS_INSTANCE" == "t2.medium" ]
 then
    echo "Instance is t2.medium, 2 vCPU"
    JOBS=2
elif [ "$TS_INSTANCE" == "c4.xlarge" ]
 then
    echo "Instance is c4.xlarge, 4 vCPU"
    JOBS=4
elif [ "$TS_INSTANCE" == "c4.2xlarge" ]
 then
    echo "Instance is c4.2xlarge, 8 vCPU"
    JOBS=8
fi


# We make sure we got the values, otherwise we abort mission
COUNTER=0
MAIN_SCRIPT="main.new.py"

cd /home/ubuntu/tap
rm -rf var/archive/
python3 ${MAIN_SCRIPT} -n ${TS_NODES} -t ${TS_TIME} -to ${TS_TIMEOUT} -s ${TS_SIZE} -ns ${TS_SPEED} -np ${TS_PAUSE} destroy

date > /home/ubuntu/foo.txt

export NS3_HOME=/home/ubuntu/workspace/source/ns-3.26

CMD="python3 ${MAIN_SCRIPT} -n ${TS_NODES} -t ${TS_TIME} -to ${TS_TIMEOUT} -s ${TS_SIZE} -ns ${TS_SPEED} -np ${TS_PAUSE}  -c ${COUNTER} -j ${JOBS} create"
echo ${CMD}
${CMD}

CMD="python3 ${MAIN_SCRIPT} -n ${TS_NODES} -t ${TS_TIME} -to ${TS_TIMEOUT} -s ${TS_SIZE} -ns ${TS_SPEED} -np ${TS_PAUSE}  -c ${COUNTER} -j ${JOBS} ns3"
echo ${CMD}
${CMD}

while [  ${COUNTER} -lt ${TS_CYCLES} ]; do

    if [ ! -f /home/ubuntu/stop.txt ]; then
        cd /home/ubuntu/tap
        DATENOW=$(date +"%y_%m_%d_%H_%M_%S")
        echo "---------------------------"
        echo ${DATENOW}
        echo "var/archive/${DATENOW}"
        echo "---------------------------"
        mkdir -p var/archive/${DATENOW}
        mv var/log/* var/archive/${DATENOW}/

#        CMD="python3 ${MAIN_SCRIPT} -n ${TS_NODES} -t ${TS_TIME} -to ${TS_TIMEOUT} -s ${TS_SIZE} -ns ${TS_SPEED} -np ${TS_PAUSE}  -c ${COUNTER} -j ${JOBS} emulation"
        CMD="python3 ${MAIN_SCRIPT} -n ${TS_NODES} -t 20 -to ${TS_TIMEOUT} -s ${TS_SIZE} -ns ${TS_SPEED} -np ${TS_PAUSE}  -c ${COUNTER} -j ${JOBS} emulation"
        echo ${CMD}
        ${CMD}

        sleep 5

        greprc=1
        while [ ${greprc} -eq 1 ]; do
            grep -r "PLEASE_EXIT=1234" var/log/*
            greprc=$?
            echo "Waiting..."
            sleep 2
        done

        cd /home/ubuntu/EC2TestAutomator
        CMD2="python3 statscollector2.py -ns ${TS_SPEED} -np ${TS_PAUSE} ${TS_NAME} ${TS_NODES} ${TS_TIME} ${TS_TIMEOUT} ${TS_SIZE}"
        echo ${CMD2}
#        ${CMD2}
    fi

	let COUNTER=COUNTER+1
	echo ${COUNTER} >> /home/ubuntu/foo.txt
done

cd /home/ubuntu/tap
CMD="python3 ${MAIN_SCRIPT} -n ${TS_NODES} -t ${TS_TIME} -to ${TS_TIMEOUT} -s ${TS_SIZE} -ns ${TS_SPEED} -np ${TS_PAUSE}  -c ${COUNTER} -j ${JOBS} destroy"
echo ${CMD}
${CMD}

date >> /home/ubuntu/foo.txt
echo ${TS_NODES} >> /home/ubuntu/foo.txt
echo ${TS_TIME} >> /home/ubuntu/foo.txt
echo ${TS_CYCLES} >> /home/ubuntu/foo.txt
echo "Done!" >> /home/ubuntu/foo.txt

DAY=$(date '+%d')
MONTH=$(date '+%m')
YEAR=$(date '+%Y')

export PATH=/home/ubuntu/.local/bin/:$PATH

cp /home/ubuntu/EC2TestAutomator/logfile.txt /home/ubuntu/${TS_NAME}.log
aws s3 cp /home/ubuntu/${TS_NAME}.log s3://treesip/${YEAR}/${MONTH}/${DAY}/${TS_NAME}/

echo "Waiting to complete ..."
sleep 2m

if [ ! -f /home/ubuntu/continue.txt ]; then
    echo "POWEROFF ..."
    poweroff
else
    echo "NOT POWEROFF ..."
fi