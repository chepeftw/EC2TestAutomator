#!/usr/bin/env bash

awsTreesip() {
Name="$1"
EmulationName="$2"
Cycles="$3"
Nodes="$4"
Size="$5"
Timeemu="$6"
InstType="$7"
Speed="$8"
CryptoPiece="$9"

AMI_SINGLE="ami-cfbb49b7"

aws ec2 run-instances \
	--image-id ${AMI_SINGLE} \
	--count 1 \
	--instance-type ${InstType} \
	--key-name SelfieServerv2 \
	--security-group-ids sg-f7b4378c \
	--subnet-id subnet-d6607ba2 \
	--associate-public-ip-address \
	--instance-initiated-shutdown-behavior terminate \
	--tag-specifications \
	"ResourceType=instance,Tags=[{Key=Name,Value=${Name}},{Key=EmulationName,Value=${EmulationName}},{Key=Cycles,Value=${Cycles}},{Key=Nodes,Value=${Nodes}},{Key=Size,Value=${Size}},{Key=Timeemu,Value=${Timeemu}},{Key=Timeout,Value=50},{Key=Speed,Value=${Speed}},{Key=Pause,Value=0},{Key=CryptoPiece,Value=${CryptoPiece}}]"
}

printAndCall() {
    CMD="$1"
    echo ${CMD}
    ${CMD}
}

# Timeout Test for 20 nodes
CCLES=50
# awsTreesip Name EmulationName Cycles Nodes Size TimeEmu Timeout Speed Pause InstanceType


#20 -> 316
#30 -> 387
#40 -> 447
#50 -> 500
#60 -> 548

runOneEmulation() {
CPIECE="$1"
NODESNUM="$2"
SIZEN="$3"
EC2TYPE="$4"
EC2TYPE_SIMPLE="$5"

EMUNAME="BlockchainPOW1_${NODESNUM}_${CPIECE}_${EC2TYPE_SIMPLE}"
printAndCall "awsTreesip BlockchainPOW1_${NODESNUM}_${CPIECE} ${EMUNAME} ${CCLES} ${NODESNUM} ${SIZEN} 20 ${EC2TYPE} 2 ${CPIECE}"

}

runMultipleEmulation() {
CPIECE="$1"

#runOneEmulation ${CPIECE} 20 316 t2.micro micro
#runOneEmulation ${CPIECE} 30 387 t2.micro micro
#runOneEmulation ${CPIECE} 40 447 t2.micro micro

runOneEmulation ${CPIECE} 20 316 t2.small small
runOneEmulation ${CPIECE} 30 387 t2.small small
runOneEmulation ${CPIECE} 40 447 t2.small small

runOneEmulation ${CPIECE} 20 316 t2.medium medium
runOneEmulation ${CPIECE} 30 387 t2.medium medium
runOneEmulation ${CPIECE} 40 447 t2.medium medium

}

#runMultipleEmulation 00
#runMultipleEmulation 000
runMultipleEmulation 0000
#runMultipleEmulation 12
#runMultipleEmulation 123
#runMultipleEmulation 1234
