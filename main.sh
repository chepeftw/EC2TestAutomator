#!/bin/bash

# Make the script to run at boot time
# chmod 744 /home/ubuntu/EC2TestAutomator/main.sh
# sudo cp treesip.service /etc/systemd/system/
# chmod 664 /etc/systemd/system/treesip.service
# systemctl daemon-reload
# systemctl enable treesip.service

# To test
# systemctl start treesip.service

# First, we get the instance ID, this IP is fixed, is not dependant on anything
INSTANCE=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
# Then based on the Instance ID, we get all tags
TAGS=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE" --output=text)

# Then we select the tag we need
FOO=$(echo "$TAGS" | grep Foo | cut -f5)

echo $FOO >> /home/ubuntu/foo.txt