#!/bin/bash
echo ""
echo "Downloading files..."
echo ""
wget https://raw.githubusercontent.com/Bunn/pi_monitor/master/pi-monitor.py
wget https://raw.githubusercontent.com/Bunn/pi_monitor/master/pi-monitor.service

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
