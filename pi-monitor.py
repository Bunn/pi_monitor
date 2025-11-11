import subprocess
import re
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import psutil


class Monitor:

    def get_soc_temperature(self):
        """Get SoC temperature using multiple fallback methods"""
        
        # Method 1: Try vcgencmd (if available)
        vcgencmd_paths = [
            "vcgencmd",
            "/usr/bin/vcgencmd",
            "/opt/vc/bin/vcgencmd"
        ]
        
        for cmd_path in vcgencmd_paths:
            try:
                result = subprocess.run(
                    [cmd_path, "measure_temp"],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                if result.returncode == 0:
                    temp_match = re.findall(r'\d+\.\d+', result.stdout)
                    if temp_match:
                        return float(temp_match[0])
            except:
                continue
        
        # Method 2: Read from thermal zone (more reliable on modern systems)
        thermal_zones = [
            "/sys/class/thermal/thermal_zone0/temp",
            "/sys/devices/virtual/thermal/thermal_zone0/temp"
        ]
        
        for zone_path in thermal_zones:
            try:
                with open(zone_path, "r") as f:
                    temp = float(f.read().strip()) / 1000.0
                    return temp
            except:
                continue
        
        print("Error: Could not read SoC temperature from any source")
        return None

    def get_gpu_temperature(self):
        return self.get_soc_temperature()

    def get_uptime(self):
        try:
            with open("/proc/uptime", "r") as file:
                uptime = file.read().strip()
            return float(uptime.split(" ")[0])
        except Exception as e:
            print(f"Error reading uptime: {e}")
            return None

    def get_load_average(self):
        try:
            load_avg = subprocess.check_output(["uptime"]).decode("utf8")
            load_average = load_avg.split("load average:")[1].split(",")
            return list(map(float, load_average))
        except Exception as e:
            print(f"Error reading load average: {e}")
            return None

    def get_kernel_release(self):
        try:
            return subprocess.check_output(["uname", "-r"]).decode("utf8").strip()
        except Exception as e:
            print(f"Error reading kernel release: {e}")
            return None

    def get_memory_usage(self):
        try:
            with open("/proc/meminfo", "r") as file:
                meminfo = file.read().strip()
            memory_usage = meminfo.split("\n")

            total_memory = next(x for x in memory_usage if 'MemTotal' in x)
            free_memory = next(x for x in memory_usage if 'MemFree' in x)
            available_memory = next(x for x in memory_usage if 'MemAvailable' in x)

            total_memory = int(re.findall(r'\d+', total_memory)[0])
            free_memory = int(re.findall(r'\d+', free_memory)[0])
            available_memory = int(re.findall(r'\d+', available_memory)[0])

            return {
                "total_memory": total_memory,
                "free_memory": free_memory,
                "available_memory": available_memory,
                "used_memory": total_memory - available_memory,
                "percent": round((total_memory - available_memory) / total_memory * 100, 2)
            }
        except Exception as e:
            print(f"Error reading memory usage: {e}")
            return None

    def get_cpu_usage(self):
        try:
            return psutil.cpu_percent(interval=1)
        except Exception as e:
            print(f"Error reading CPU usage: {e}")
            return None

    def get_disk_usage(self):
        try:
            disk_usage = psutil.disk_usage('/')
            return {
                "total": disk_usage.total,
                "used": disk_usage.used,
                "free": disk_usage.free,
                "percent": disk_usage.percent
            }
        except Exception as e:
            print(f"Error reading disk usage: {e}")
            return None

    def get_network_stats(self):
        try:
            net_io = psutil.net_io_counters()
            return {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv
            }
        except Exception as e:
            print(f"Error reading network stats: {e}")
            return None

    def get_json(self):
        data = {
            "thermal_temperature": self.get_thermal_temperature(),
            "soc_temperature": self.get_soc_temperature(),
            "gpu_temperature": self.get_gpu_temperature(),
            "uptime": self.get_uptime(),
            "load_average": self.get_load_average(),
            "kernel_release": self.get_kernel_release(),
            "memory": self.get_memory_usage(),
            "cpu_usage": self.get_cpu_usage(),
            "disk_usage": self.get_disk_usage(),
            "network_stats": self.get_network_stats()
        }
        return json.dumps(data, indent=2)


class MonitorServer(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        """Override to reduce console spam"""
        return

    def set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        if self.path in ["/monitor.json", "/monitor", "/"]:
            self.set_response()
            response = Monitor().get_json().encode()
            self.wfile.write(response)
            print(f"Served monitor data to {self.client_address[0]}")
        else:
            self.send_error(404, "Not Found")


def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MonitorServer)
    print(f"Starting monitor server on port {port}")
    print(f"Access the monitor at: http://localhost:{port}/monitor.json")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()


if __name__ == "__main__":
    port = 8088
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    
    # Test the monitor once before starting server
    print("Testing monitor functions...")
    m = Monitor()
    temp = m.get_soc_temperature()
    if temp:
        print(f"✓ Temperature reading works: {temp}°C")
    else:
        print("⚠ Temperature reading failed")
    
    run_server(port)