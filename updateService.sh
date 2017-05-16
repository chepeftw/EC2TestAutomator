#!/bin/bash -

# Update service but run it as root
chmod +x /home/ubuntu/EC2TestAutomator/main.sh
chmod +x /home/ubuntu/run.sh
cp treesip.service /etc/systemd/system/
chmod 664 /etc/systemd/system/treesip.service
systemctl daemon-reload
systemctl enable treesip.service