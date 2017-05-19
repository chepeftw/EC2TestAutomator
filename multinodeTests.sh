#!/bin/bash -

awsTreesip() {
Name="$1"
EmulationName="$2"
Cycles="$3"
Nodes="$4"
Size="$5"
Timeemu="$6"
Timeout="$7"
Speed="$8"
Pause="$9"

AMI_MULTI="ami-6bc7a10b"
ITYPE="t2.micro"

case "$Nodes" in
"40") ITYPE="t2.small"
   ;;
"50") ITYPE="t2.medium"
   ;;
"60") ITYPE="t2.medium"
    ;;
"70") ITYPE="t2.large"
    ;;
"80") ITYPE="t2.large"
    ;;
"90") ITYPE="t2.large"
    ;;
"100") ITYPE="t2.xlarge"
    ;;
esac

aws ec2 run-instances \
	--image-id $AMI_MULTI \
	--count 1 \
	--instance-type $ITYPE \
	--key-name SelfieServerv2 \
	--security-group-ids sg-f7b4378c \
	--subnet-id subnet-d6607ba2 \
	--associate-public-ip-address \
	--instance-initiated-shutdown-behavior terminate \
	--tag-specifications \
	"ResourceType=instance,Tags=[{Key=Name,Value=$Name},{Key=EmulationName,Value=$EmulationName},{Key=Cycles,Value=$Cycles},{Key=Nodes,Value=$Nodes},{Key=Size,Value=$Size},{Key=Timeemu,Value=$Timeemu},{Key=Timeout,Value=$Timeout},{Key=Speed,Value=$Speed},{Key=Pause,Value=$Pause}]"
}

# Timeout Test for 20 nodes
COUNTER=1
while [  $COUNTER -lt 6 ]; do
    let SPEED=COUNTER*2
    # awsTreesip Name EmulationName Cycles Nodes Size TimeEmu Timeout Speed Pause InstanceType
#    awsTreesip TreesipMulti TestMultiN_20_$SPEED 200 20 300 45 200 $SPEED 0
    awsTreesip TreesipMulti MultiN_20_$SPEED 200 20 300 45 200 $SPEED 0
    awsTreesip TreesipMulti MultiN_30_$SPEED 200 30 350 55 200 $SPEED 0
    awsTreesip TreesipMulti MultiN_40_$SPEED 200 40 400 65 200 $SPEED 0
    awsTreesip TreesipMulti MultiN_50_$SPEED 200 50 450 75 200 $SPEED 0
    awsTreesip TreesipMulti MultiN_60_$SPEED 200 60 500 85 200 $SPEED 0
    awsTreesip TreesipMulti MultiN_70_$SPEED 200 70 550 95 200 $SPEED 0
    awsTreesip TreesipMulti MultiN_80_$SPEED 200 80 600 105 200 $SPEED 0
    awsTreesip TreesipMulti MultiN_90_$SPEED 200 90 650 115 200 $SPEED 0
    awsTreesip TreesipMulti MultiN_100_$SPEED 200 100 650 125 200 $SPEED 0
	let COUNTER=COUNTER+1
done
