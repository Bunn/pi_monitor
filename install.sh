#!/bin/bash
echo "Downloading files..."
wget https://raw.githubusercontent.com/Bunn/pi_monitor/master/pi_monitor.py
wget https://raw.githubusercontent.com/Bunn/pi_monitor/master/pi-monitor.service

echo "Moving files..."
mv pi_monitor.py /usr/local/bin/
mv pi-monitor.service /etc/systemd/system/

echo "Starting pi-monitor service..."
systemctl start pi-monitor.service
