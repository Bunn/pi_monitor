# Pi Monitor

Pi Monitor is a Python utility designed to provide various metrics from a Raspberry Pi. This experimental tool offers a simple HTTP server that delivers Raspberry Pi metrics via RESTful API calls, including temperature, load average, and more. Use it at your own risk.

## Features

- Provides metrics such as SoC temperature, GPU temperature, uptime, load average, kernel release, memory usage, CPU usage, disk usage, and network statistics.
- Runs a simple HTTP server to serve these metrics in JSON format.

## Usage

The server exposes a single endpoint on the default port `8088`:
- Access it via `http://YOUR_IP:8088/monitor.json` to receive a JSON response with the following structure:

```json
{
  "soc_temperature": 50.5,
  "gpu_temperature": 50.5,
  "uptime": 18551.34,
  "load_average": [0.0, 0.2, 0.1],
  "kernel_release": "5.4.51-v7+",
  "memory": {
    "total_memory": 441416,
    "free_memory": 90536,
    "available_memory": 279512
  },
  "cpu_usage": 15.0,
  "disk_usage": {
    "total": 1000000000,
    "used": 500000000,
    "free": 500000000,
    "percent": 50.0
  },
  "network_stats": {
    "bytes_sent": 123456,
    "bytes_recv": 654321,
    "packets_sent": 1234,
    "packets_recv": 4321
  }
}
```

## Installation

### Automatic Installation

To install Pi Monitor automatically, run the following command:

```bash
wget -O - https://raw.githubusercontent.com/Bunn/pi_monitor/master/install.sh | sudo bash
```

### Manual Installation

For manual installation, download the necessary files and execute the script as desired. If you prefer not to run Pi Monitor as a service, you can execute it directly using:

```bash
python3 pi_monitor.py
```

## Configuration

### Service Configuration

If you installed Pi Monitor using the automatic method, you can modify the username and default port by editing the `pi-monitor.service` file:

```ini
[Service]
ExecStart=/usr/bin/python3 -u /usr/local/bin/pi-monitor.py 8088
User=pi
```

To apply changes, stop the service with:

```bash
sudo systemctl stop pi-monitor.service
```

Then, restart it with:

```bash
sudo systemctl start pi-monitor.service
```

### Manual Configuration

If running manually, change the default port by passing it as a parameter:

```bash
python3 pi_monitor.py 8181
```

## Compatibility

Pi Monitor has been tested on Raspberry Pi OS (32-bit) with kernel version 5.4.51-v7+.
