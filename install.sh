#!/bin/bash
systemctl stop pi-monitor.service

echo ""
echo "Downloading files..."
echo ""
wget https://raw.githubusercontent.com/Bunn/pi_monitor/master/pi-monitor.py
wget https://raw.githubusercontent.com/Bunn/pi_monitor/master/pi-monitor.service

echo ""
echo "Removing old files files..."
echo ""
rm /usr/local/bin/pi-monitor.py
rm /etc/systemd/system/pi-monitor.service

echo ""
echo "Moving files..."
echo ""
mv pi-monitor.py /usr/local/bin/
mv pi-monitor.service /etc/systemd/system/

echo ""
echo "Starting pi-monitor service..."
echo ""
systemctl daemon-reload
systemctl start pi-monitor.service
systemctl enable pi-monitor.service 