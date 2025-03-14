import subprocess
import re
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import psutil


class Monitor:

    def get_soc_temperature(self):
        try:
            temp = subprocess.check_output(
                ["vcgencmd", "measure_temp"]).decode("utf8")
            return float(re.findall(r'\d+\.\d+', temp)[0])
        except Exception as e:
            print(f"Error reading SoC temperature: {e}")
            return None

    def get_gpu_temperature(self):
        try:
            temp = subprocess.check_output(
                ["vcgencmd", "measure_temp"]).decode("utf8")
            return float(re.findall(r'\d+\.\d+', temp)[0])
        except Exception as e:
            print(f"Error reading GPU temperature: {e}")
            return None

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
                "available_memory": available_memory
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
        return json.dumps(data)


class MonitorServer(BaseHTTPRequestHandler):

    def set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self.set_response()
        if self.path in ["/monitor.json", "/monitor"]:
            response = Monitor().get_json().encode()
            self.wfile.write(response)


def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MonitorServer)
    print(f"Starting server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    port = 8088
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(port)
