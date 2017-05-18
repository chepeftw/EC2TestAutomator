#!/bin/bash -

awsTreesip() {
Name="$1"
EmulationName="$2"
Cycles="$3"
Nodes="$4"
Size="$5"
Timeemu="$6"
Timeout="$7"

AMI_SINGLE="ami-5b43253b"
AMI_MULTIN="ami-994026f9"

aws ec2 run-instances \
	--image-id $AMI_SINGLE \
	--count 1 \
	--instance-type t2.micro \
	--key-name SelfieServerv2 \
	--security-group-ids sg-f7b4378c \
	--subnet-id subnet-d6607ba2 \
	--associate-public-ip-address \
	--instance-initiated-shutdown-behavior terminate \
	--tag-specifications \
	"ResourceType=instance,Tags=[{Key=Name,Value=$Name},{Key=EmulationName,Value=$EmulationName},{Key=Cycles,Value=$Cycles},{Key=Nodes,Value=$Nodes},{Key=Size,Value=$Size},{Key=Timeemu,Value=$Timeemu},{Key=Timeout,Value=$Timeout}]"
}

## Timeout Test for 20 nodes
COUNTER=1
while [  $COUNTER -lt 11 ]; do
    let TMOUT=COUNTER*100
    awsTreesip TreesipTmout Tmout_20_$TMOUT 100 20 300 40 $TMOUT
	let COUNTER=COUNTER+1
done
awsTreesip TreesipTmout Tmout_20_1200 100 20 300 40 1200
awsTreesip TreesipTmout Tmout_20_1400 100 20 300 40 1400
awsTreesip TreesipTmout Tmout_20_1600 100 20 300 40 1600
awsTreesip TreesipTmout Tmout_20_1800 100 20 300 40 1800

## Timeout Test for 30 nodes
COUNTER=1
while [  $COUNTER -lt 11 ]; do
    let TMOUT=COUNTER*100
    awsTreesip TreesipTmout Tmout_30_$TMOUT 100 30 400 50 $TMOUT
	let COUNTER=COUNTER+1
done
awsTreesip TreesipTmout Tmout_30_1200 100 30 400 50 1200
awsTreesip TreesipTmout Tmout_30_1400 100 30 400 50 1400
awsTreesip TreesipTmout Tmout_30_1600 100 30 400 50 1600
awsTreesip TreesipTmout Tmout_30_1800 100 30 400 50 1800

## Timeout Test for 40 nodes
COUNTER=1
while [  $COUNTER -lt 11 ]; do
    let TMOUT=COUNTER*100
    awsTreesip TreesipTmout Tmout_40_$TMOUT 100 40 500 60 $TMOUT
	let COUNTER=COUNTER+1
done
awsTreesip TreesipTmout Tmout_40_1200 100 40 500 60 1200
awsTreesip TreesipTmout Tmout_40_1400 100 40 500 60 1400
awsTreesip TreesipTmout Tmout_40_1600 100 40 500 60 1600
awsTreesip TreesipTmout Tmout_40_1800 100 40 500 60 1800

## Timeout Test for 50 nodes
COUNTER=1
while [  $COUNTER -lt 11 ]; do
    let TMOUT=COUNTER*100
    awsTreesip TreesipTmout Tmout_50_$TMOUT 100 50 600 70 $TMOUT
	let COUNTER=COUNTER+1
done
awsTreesip TreesipTmout Tmout_50_1200 100 50 600 70 1200
awsTreesip TreesipTmout Tmout_50_1400 100 50 600 70 1400
awsTreesip TreesipTmout Tmout_50_1600 100 50 600 70 1600
awsTreesip TreesipTmout Tmout_50_1800 100 50 600 70 1800

## Timeout Test for 60 nodes
COUNTER=1
while [  $COUNTER -lt 11 ]; do
    let TMOUT=COUNTER*100
    awsTreesip TreesipTmout Tmout_60_$TMOUT 100 60 700 80 $TMOUT
	let COUNTER=COUNTER+1
done
awsTreesip TreesipTmout Tmout_60_1200 100 60 700 80 1200
awsTreesip TreesipTmout Tmout_60_1400 100 60 700 80 1400
awsTreesip TreesipTmout Tmout_60_1600 100 60 700 80 1600
awsTreesip TreesipTmout Tmout_60_1800 100 60 700 80 1800