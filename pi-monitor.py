import subprocess
import re
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class Monitor:

    def get_thermal_temperature(self):
        thermal = subprocess.check_output(
            "cat /sys/class/thermal/thermal_zone0/temp", shell=True).decode("utf8")
        return float(thermal) / 1000.0

    # returns the temperature of the SoC as measured by the on-board temperature sensor
    def get_soc_temperature(self):
        temp = subprocess.check_output(
            "vcgencmd measure_temp", shell=True).decode("utf8")
        return float(re.findall(r'\d+\.\d+', temp)[0])

    # uptime in seconds
    def get_uptime(self):
        uptime = subprocess.check_output(
            "cat /proc/uptime", shell=True).decode("utf8")
        return float(uptime.split(" ")[0])

    # returns load averages for 1, 5, and 15 minutes
    def get_load_average(self):
        uptime = subprocess.check_output("uptime", shell=True).decode("utf8")
        load_average = uptime.split("load average:")[1].split(",")
        return list(map(float, load_average))

    def get_kernel_release(self):
        return subprocess.check_output("uname -r", shell=True).decode("utf8").strip()

    def get_json(self):
        data = {
            "soc_temperature": self.get_soc_temperature(),
            "uptime": self.get_uptime(),
            "load_average": self.get_load_average(),
            "kernel_release": self.get_kernel_release()
        }
        return json.dumps(data)


class MonitorServer(BaseHTTPRequestHandler):

    def set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self.set_response()
        print(self.path)
        if self.path == "/monitor.json" or self.path == "/monitor":
            response = Monitor().get_json().encode()
            self.wfile.write(response)


port = 8088
server_address = ('', port)
httpd = HTTPServer(server_address, MonitorServer)
httpd.serve_forever()
