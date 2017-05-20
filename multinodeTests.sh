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

AMI_MULTI="ami-10157470"
ITYPE="t2.small"

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

# awsTreesip TreesipMulti3 MultiN3_2_70_2 50 70 550 95 200 2 0
# awsTreesip TreesipMulti3 MultiN3_2_70_3 50 70 500 95 200 2 0

# awsTreesip TreesipMulti7 MultiN7_50_2 200 50 450 130 800 2 0

 Timeout Test for 20 nodes
COUNTER=1
TOUT=600
CCLES=100
while [  $COUNTER -lt 6 ]; do
    NODESN=20
    SIZEN=300
    let SPEED=COUNTER*2
    while [  $NODESN -lt 60 ]; do
        let TIMEEMU=NODESN*2
        let TIMEEMU=TIMEEMU+30
            EMUNAME="MultiN8_"$NODESN"_"$SPEED
            # awsTreesip Name EmulationName Cycles Nodes Size TimeEmu Timeout Speed Pause InstanceType
            CMD="awsTreesip TreesipMulti8 $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"
            echo $CMD
            $CMD

        let NODESN=NODESN+10
        let SIZEN=SIZEN+50
    done
	let COUNTER=COUNTER+1
done


# MultiN7_ - I fixed the sync problem by setting in the main.py to 2*1 times the nodes number, and the total emu time for
#               NS3 is 2 times nodes number plus 30, there should be a MUCH BETTER way of syncing the instances
#               but for now that should do it, before this tests the simulations could be questionable I guess

# MultiN8_ - I will centralize logs now to check if something fails.