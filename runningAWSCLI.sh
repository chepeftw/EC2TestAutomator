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
awsTreesip TimeoutTest TimeoutTest_20_100 100 20 300 40 100
awsTreesip TimeoutTest TimeoutTest_20_200 100 20 300 40 200
awsTreesip TimeoutTest TimeoutTest_20_300 100 20 300 40 300
awsTreesip TimeoutTest TimeoutTest_20_400 100 20 300 40 400
awsTreesip TimeoutTest TimeoutTest_20_500 100 20 300 40 500
awsTreesip TimeoutTest TimeoutTest_20_600 100 20 300 40 600
awsTreesip TimeoutTest TimeoutTest_20_700 100 20 300 40 700
awsTreesip TimeoutTest TimeoutTest_20_800 100 20 300 40 800
awsTreesip TimeoutTest TimeoutTest_20_900 100 20 300 40 900
awsTreesip TimeoutTest TimeoutTest_20_1000 100 20 300 40 1000
awsTreesip TimeoutTest TimeoutTest_20_1200 100 20 300 40 1200
awsTreesip TimeoutTest TimeoutTest_20_1400 100 20 300 40 1400
awsTreesip TimeoutTest TimeoutTest_20_1600 100 20 300 40 1600
awsTreesip TimeoutTest TimeoutTest_20_1800 100 20 300 40 1800

## Timeout Test for 30 nodes
awsTreesip TimeoutTest TimeoutTest_30_100 100 30 400 50 100
awsTreesip TimeoutTest TimeoutTest_30_200 100 30 400 50 200
awsTreesip TimeoutTest TimeoutTest_30_300 100 30 400 50 300
awsTreesip TimeoutTest TimeoutTest_30_400 100 30 400 50 400
awsTreesip TimeoutTest TimeoutTest_30_500 100 30 400 50 500

## it broke here due to the instance limit

awsTreesip TimeoutTest TimeoutTest_30_600 100 30 400 50 600
awsTreesip TimeoutTest TimeoutTest_30_700 100 30 400 50 700
awsTreesip TimeoutTest TimeoutTest_30_800 100 30 400 50 800
awsTreesip TimeoutTest TimeoutTest_30_900 100 30 400 50 900
awsTreesip TimeoutTest TimeoutTest_30_1000 100 30 400 50 1000
awsTreesip TimeoutTest TimeoutTest_30_1200 100 30 400 50 1200
awsTreesip TimeoutTest TimeoutTest_30_1400 100 30 400 50 1400
awsTreesip TimeoutTest TimeoutTest_30_1600 100 30 400 50 1600
awsTreesip TimeoutTest TimeoutTest_30_1800 100 30 400 50 1800

## Timeout Test for 40 nodes
awsTreesip TimeoutTest TimeoutTest_40_100 100 40 500 60 100
awsTreesip TimeoutTest TimeoutTest_40_200 100 40 500 60 200
awsTreesip TimeoutTest TimeoutTest_40_300 100 40 500 60 300
awsTreesip TimeoutTest TimeoutTest_40_400 100 40 500 60 400
awsTreesip TimeoutTest TimeoutTest_40_500 100 40 500 60 500
awsTreesip TimeoutTest TimeoutTest_40_600 100 40 500 60 600
awsTreesip TimeoutTest TimeoutTest_40_700 100 40 500 60 700
awsTreesip TimeoutTest TimeoutTest_40_800 100 40 500 60 800
awsTreesip TimeoutTest TimeoutTest_40_900 100 40 500 60 900
awsTreesip TimeoutTest TimeoutTest_40_1000 100 40 500 60 1000
awsTreesip TimeoutTest TimeoutTest_40_1200 100 40 500 60 1200
awsTreesip TimeoutTest TimeoutTest_40_1400 100 40 500 60 1400
awsTreesip TimeoutTest TimeoutTest_40_1600 100 40 500 60 1600
awsTreesip TimeoutTest TimeoutTest_40_1800 100 40 500 60 1800

## Timeout Test for 50 nodes
awsTreesip TimeoutTest TimeoutTest_50_100 100 50 600 70 100
awsTreesip TimeoutTest TimeoutTest_50_200 100 50 600 70 200
awsTreesip TimeoutTest TimeoutTest_50_300 100 50 600 70 300
awsTreesip TimeoutTest TimeoutTest_50_400 100 50 600 70 400
awsTreesip TimeoutTest TimeoutTest_50_500 100 50 600 70 500
awsTreesip TimeoutTest TimeoutTest_50_600 100 50 600 70 600
awsTreesip TimeoutTest TimeoutTest_50_700 100 50 600 70 700
awsTreesip TimeoutTest TimeoutTest_50_800 100 50 600 70 800
awsTreesip TimeoutTest TimeoutTest_50_900 100 50 600 70 900
awsTreesip TimeoutTest TimeoutTest_50_1000 100 50 600 70 1000
awsTreesip TimeoutTest TimeoutTest_50_1200 100 50 600 70 1200
awsTreesip TimeoutTest TimeoutTest_50_1400 100 50 600 70 1400
awsTreesip TimeoutTest TimeoutTest_50_1600 100 50 600 70 1600
awsTreesip TimeoutTest TimeoutTest_50_1800 100 50 600 70 1800

## Timeout Test for 60 nodes
awsTreesip TimeoutTest TimeoutTest_60_100 100 60 700 80 100
awsTreesip TimeoutTest TimeoutTest_60_200 100 60 700 80 200
awsTreesip TimeoutTest TimeoutTest_60_300 100 60 700 80 300
awsTreesip TimeoutTest TimeoutTest_60_400 100 60 700 80 400
awsTreesip TimeoutTest TimeoutTest_60_500 100 60 700 80 500
awsTreesip TimeoutTest TimeoutTest_60_600 100 60 700 80 600
awsTreesip TimeoutTest TimeoutTest_60_700 100 60 700 80 700
awsTreesip TimeoutTest TimeoutTest_60_800 100 60 700 80 800
awsTreesip TimeoutTest TimeoutTest_60_900 100 60 700 80 900
awsTreesip TimeoutTest TimeoutTest_60_1000 100 60 700 80 1000
awsTreesip TimeoutTest TimeoutTest_60_1200 100 60 700 80 1200
awsTreesip TimeoutTest TimeoutTest_60_1400 100 60 700 80 1400
awsTreesip TimeoutTest TimeoutTest_60_1600 100 60 700 80 1600
awsTreesip TimeoutTest TimeoutTest_60_1800 100 60 700 80 1800