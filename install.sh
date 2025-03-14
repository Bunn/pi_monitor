#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

SERVICE_NAME="pi-monitor.service"
SCRIPT_NAME="pi-monitor.py"
SERVICE_URL="https://raw.githubusercontent.com/Bunn/pi_monitor/master/$SERVICE_NAME"
SCRIPT_URL="https://raw.githubusercontent.com/Bunn/pi_monitor/master/$SCRIPT_NAME"
BIN_DIR="/usr/local/bin"
SYSTEMD_DIR="/etc/systemd/system"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

download_file() {
    local url=$1
    local dest=$2
    if wget -q "$url" -O "$dest"; then
        log "Downloaded $dest successfully."
    else
        log "Failed to download $dest."
        exit 1
    fi
}

remove_file() {
    local file=$1
    if [ -f "$file" ]; then
        rm "$file"
        log "Removed $file."
    else
        log "$file does not exist, skipping removal."
    fi
}

move_file() {
    local src=$1
    local dest=$2
    mv "$src" "$dest"
    log "Moved $src to $dest."
}

log "Stopping $SERVICE_NAME if it's running..."
if systemctl is-active --quiet $SERVICE_NAME; then
    systemctl stop $SERVICE_NAME
    log "$SERVICE_NAME stopped."
else
    log "$SERVICE_NAME is not running."
fi

echo ""

log "Downloading files..."
download_file "$SCRIPT_URL" "$SCRIPT_NAME"
download_file "$SERVICE_URL" "$SERVICE_NAME"

echo ""

log "Removing old files..."
remove_file "$BIN_DIR/$SCRIPT_NAME"
remove_file "$SYSTEMD_DIR/$SERVICE_NAME"

echo ""

log "Moving files..."
move_file "$SCRIPT_NAME" "$BIN_DIR/"
move_file "$SERVICE_NAME" "$SYSTEMD_DIR/"

echo ""

log "Reloading systemd daemon and starting $SERVICE_NAME..."
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME
log "$SERVICE_NAME started and enabled."

log "Installation complete."
