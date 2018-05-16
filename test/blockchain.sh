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
Timeout="$9"

AMI_SINGLE="ami-016636ace955cba2f"

bash awscli.sh ec2 run-instances \
	--image-id ${AMI_SINGLE} \
	--count 1 \
	--instance-type ${InstType} \
	--key-name SelfieServerv2 \
	--security-group-ids sg-f7b4378c \
	--subnet-id subnet-d6607ba2 \
	--associate-public-ip-address \
	--instance-initiated-shutdown-behavior terminate \
	--tag-specifications \
	"ResourceType=instance,Tags=[{Key=Name,Value=${Name}},{Key=EmulationName,Value=${EmulationName}},{Key=Cycles,Value=${Cycles}},{Key=Nodes,Value=${Nodes}},{Key=Size,Value=${Size}},{Key=Timeemu,Value=${Timeemu}},{Key=Timeout,Value=${Timeout}},{Key=Speed,Value=${Speed}},{Key=Pause,Value=0}]"
}

printAndCall() {
    CMD="$1"
    echo ${CMD}
    ${CMD}
}

# Timeout Test for 20 nodes
CCLES=200
# awsTreesip Name EmulationName Cycles Nodes Size TimeEmu Timeout Speed Pause InstanceType


#20 -> 316
#30 -> 387
#40 -> 447
#50 -> 500
#60 -> 548

runOneEmulation() {
TIMEOUT="$1"
NODESNUM="$2"
SIZEN="$3"
EC2TYPE="$4"
EC2TYPE_SIMPLE="$5"
SPEED="$6"

EMUNAME="Blockchain_1_${NODESNUM}_${SIZEN}_${TIMEOUT}_${SPEED}"
printAndCall "awsTreesip Blockchain_1_${NODESNUM}_${SIZEN}_${TIMEOUT}_${SPEED} ${EMUNAME} ${CCLES} ${NODESNUM} ${SIZEN} 20 ${EC2TYPE} ${SPEED} ${TIMEOUT}"

}

runMultipleEmulation() {
TIMOUT="$1"
SPEED="$2"

runOneEmulation ${TIMOUT} 20 316 t2.medium m ${SPEED}
runOneEmulation ${TIMOUT} 30 387 t2.large m ${SPEED}
runOneEmulation ${TIMOUT} 40 447 m5.large l ${SPEED}
runOneEmulation ${TIMOUT} 50 500 m5.xlarge xl ${SPEED}

runOneEmulation ${TIMOUT} 20 258 t2.medium m ${SPEED}
runOneEmulation ${TIMOUT} 30 316 t2.large m ${SPEED}
runOneEmulation ${TIMOUT} 40 365 m5.large l ${SPEED}
runOneEmulation ${TIMOUT} 50 408 m5.xlarge xl ${SPEED}

runOneEmulation ${TIMOUT} 20 365 t2.medium m ${SPEED}
runOneEmulation ${TIMOUT} 30 447 t2.large m ${SPEED}
runOneEmulation ${TIMOUT} 40 515 m5.large l ${SPEED}
runOneEmulation ${TIMOUT} 50 577 m5.xlarge xl ${SPEED}

}

runMultipleEmulation 200 2
runMultipleEmulation 200 5
runMultipleEmulation 300 2
runMultipleEmulation 300 5