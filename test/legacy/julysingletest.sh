#!/usr/bin/env bash

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

AMI_SINGLE="ami-583d5138"
ITYPE="t2.small"

case "$Nodes" in
"30") ITYPE="t2.small"
   ;;
"40") ITYPE="t2.medium"
   ;;
"50") ITYPE="c4.large"
    ;;
"60") ITYPE="c4.large"
    ;;
#"80") ITYPE="t2.large"
#    ;;
#"90") ITYPE="t2.large"
#    ;;
#"100") ITYPE="t2.xlarge"
#    ;;
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

printAndCall() {
    CMD="$1"
    echo $CMD
    #$CMD
}

# Timeout Test for 20 nodes
CCLES=100
# awsTreesip Name EmulationName Cycles Nodes Size TimeEmu Timeout Speed Pause InstanceType


#20 -> 316
#30 -> 387
#40 -> 447
#50 -> 500
#60 -> 548


COUNTER=1
TOUT=50
while [  $COUNTER -lt 6 ]; do
    let SPEED=COUNTER*2
    let TIMEEMU=NODESN*2

    let NODESN=20
    let SIZEN=316

    EMUNAME="JulySingle_"$NODESN"_"$SPEED"_"$TOUT
    printAndCall "awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"

    let NODESN=NODESN+10 #30
    let SIZEN=387

    EMUNAME="JulySingle_"$NODESN"_"$SPEED"_"$TOUT
    printAndCall "awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"

    let NODESN=NODESN+10 #40
    let SIZEN=447

    EMUNAME="JulySingle_"$NODESN"_"$SPEED"_"$TOUT
    printAndCall "awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"

    let NODESN=NODESN+10 #50
    let SIZEN=500

    EMUNAME="JulySingle_"$NODESN"_"$SPEED"_"$TOUT
    printAndCall "awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"

    let NODESN=NODESN+10 #60
    let SIZEN=548

    EMUNAME="JulySingle_"$NODESN"_"$SPEED"_"$TOUT
    printAndCall "awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"

    let COUNTER=COUNTER+1
done


COUNTER=1
TOUT=100
while [  $COUNTER -lt 6 ]; do
    let SPEED=COUNTER*2
    let TIMEEMU=NODESN*2

    let NODESN=20
    let SIZEN=316

    EMUNAME="JulySingle_"$NODESN"_"$SPEED"_"$TOUT
    printAndCall "awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"

    let NODESN=NODESN+10 #30
    let SIZEN=387

    EMUNAME="JulySingle_"$NODESN"_"$SPEED"_"$TOUT
    printAndCall "awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"

    let NODESN=NODESN+10 #40
    let SIZEN=447

    EMUNAME="JulySingle_"$NODESN"_"$SPEED"_"$TOUT
    printAndCall "awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"

    let NODESN=NODESN+10 #50
    let SIZEN=500

    EMUNAME="JulySingle_"$NODESN"_"$SPEED"_"$TOUT
    printAndCall "awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"

    let NODESN=NODESN+10 #60
    let SIZEN=548

    EMUNAME="JulySingle_"$NODESN"_"$SPEED"_"$TOUT
    printAndCall "awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"

    let COUNTER=COUNTER+1
done


COUNTERTOUT=1

while [  $COUNTERTOUT -lt 5 ]; do
    COUNTER=1
    let TOUT=COUNTERTOUT*200

    while [  $COUNTER -lt 6 ]; do
        let SPEED=COUNTER*2
        let TIMEEMU=NODESN*2

        let NODESN=20
        let SIZEN=316

        EMUNAME="JulySingle_"$NODESN"_"$SPEED"_"$TOUT
        printAndCall "awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"

        let NODESN=NODESN+10 #30
        let SIZEN=387

        EMUNAME="JulySingle_"$NODESN"_"$SPEED"_"$TOUT
        printAndCall "awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"

        let NODESN=NODESN+10 #40
        let SIZEN=447

        EMUNAME="JulySingle_"$NODESN"_"$SPEED"_"$TOUT
        printAndCall "awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"

        let NODESN=NODESN+10 #50
        let SIZEN=500

        EMUNAME="JulySingle_"$NODESN"_"$SPEED"_"$TOUT
        printAndCall "awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"

        let NODESN=NODESN+10 #60
        let SIZEN=548

        EMUNAME="JulySingle_"$NODESN"_"$SPEED"_"$TOUT
        printAndCall "awsTreesip Treesip$EMUNAME $EMUNAME $CCLES $NODESN $SIZEN $TIMEEMU $TOUT $SPEED 0"

        let COUNTER=COUNTER+1
    done

    let COUNTERTOUT=COUNTERTOUT+1
done