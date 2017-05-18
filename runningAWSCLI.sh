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
	--tag-specifications \
	"ResourceType=instance,Tags=[{Key=Name,Value=$Name},{Key=EmulationName,Value=$EmulationName},{Key=Cycles,Value=$Cycles},{Key=Nodes,Value=$Nodes},{Key=Size,Value=$Size},{Key=Timeemu,Value=$Timeemu},{Key=Timeout,Value=$Timeout}]"
}

awsTreesip CLITest1 Test001 10 20 300 40 600