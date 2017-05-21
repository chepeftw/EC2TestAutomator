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

AMI_SINGLE="ami-22563742"
ITYPE="t2.small"

case "$Nodes" in
"40") ITYPE="t2.small"
   ;;
"50") ITYPE="t2.medium"
   ;;
"60") ITYPE="t2.large"
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
	--image-id $AMI_SINGLE \
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
TOUT=600
CCLES=100
while [  $COUNTER -lt 6 ]; do
    NODESN=20
    SIZEN=300
    let SPEED=COUNTER*2
    while [  $NODESN -lt 70 ]; do
        let TIMEEMU=NODESN*2
        let TIMEEMU=TIMEEMU+30
            EMUNAME="SimpleN1_"$NODESN"_"$SPEED
            # awsTreesip Name EmulationName Cycles Nodes Size TimeEmu Timeout Speed Pause InstanceType
            CMD="awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"
            echo $CMD
            $CMD

        let NODESN=NODESN+10
        let SIZEN=SIZEN+50
    done
	let COUNTER=COUNTER+1
done

# SingleN1_ - First run using the simple AMI, I just commented the extra root node code.
#               This will help me to compare with the multinode.