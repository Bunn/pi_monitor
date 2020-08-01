#!/bin/bash
systemctl stop pi-monitor.service

echo ""

echo "Downloading files..."

wget https://raw.githubusercontent.com/Bunn/pi_monitor/master/pi-monitor.py
wget https://raw.githubusercontent.com/Bunn/pi_monitor/master/pi-monitor.service

echo ""

echo "Removing old files files..."
rm /usr/local/bin/pi-monitor.py
rm /etc/systemd/system/pi-monitor.service

echo ""

echo "Moving files..."
mv pi-monitor.py /usr/local/bin/
mv pi-monitor.service /etc/systemd/system/

echo ""

echo "Starting pi-monitor service..."
systemctl daemon-reload
systemctl enable pi-monitor.service 
systemctl start pi-monitor.service