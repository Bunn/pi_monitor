#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

SERVICE_NAME="pi-monitor.service"
SCRIPT_NAME="pi-monitor.py"
SCRIPT_URL="https://raw.githubusercontent.com/Bunn/pi_monitor/master/$SCRIPT_NAME"
BIN_DIR="/usr/local/bin"
SYSTEMD_DIR="/etc/systemd/system"
CURRENT_USER=$(whoami)

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
        if rm "$file"; then
            log "Removed $file."
        else
            log "Failed to remove $file. Trying with sudo..."
            if sudo rm "$file"; then
                log "Removed $file with sudo."
            else
                log "Failed to remove $file even with sudo."
                exit 1
            fi
        fi
    else
        log "$file does not exist, skipping removal."
    fi
}

move_file() {
    local src=$1
    local dest=$2
    if sudo mv "$src" "$dest"; then
        log "Moved $src to $dest."
    else
        log "Failed to move $src to $dest."
        exit 1
    fi
}

create_service_file() {
    local service_file_path=$1
    cat <<EOF | sudo tee "$service_file_path" > /dev/null
[Unit]
Description=Pi Monitor Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 -u $BIN_DIR/$SCRIPT_NAME 8088
User=$CURRENT_USER
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    log "Created service file at $service_file_path."
}

log "Stopping $SERVICE_NAME if it's running..."
if systemctl is-active --quiet $SERVICE_NAME; then
    sudo systemctl stop $SERVICE_NAME
    log "$SERVICE_NAME stopped."
else
    log "$SERVICE_NAME is not running."
fi

echo ""

log "Downloading script..."
download_file "$SCRIPT_URL" "$SCRIPT_NAME"

echo ""

log "Removing old files..."
remove_file "$BIN_DIR/$SCRIPT_NAME"
remove_file "$SYSTEMD_DIR/$SERVICE_NAME"

echo ""

log "Moving script..."
move_file "$SCRIPT_NAME" "$BIN_DIR/"

echo ""

log "Creating service file..."
create_service_file "$SYSTEMD_DIR/$SERVICE_NAME"

echo ""

log "Reloading systemd daemon and starting $SERVICE_NAME..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME
log "$SERVICE_NAME started and enabled."

log "Installation complete."
