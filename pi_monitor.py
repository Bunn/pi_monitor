
import subprocess
import re
import json

def get_thermal_temperature():
	thermal = subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True)
	return float(thermal) / 1000.0

#returns the temperature of the SoC as measured by the on-board temperature sensor
def get_soc_temperature():
	temp = subprocess.check_output("vcgencmd measure_temp", shell=True)
	return re.findall(r'\d+\.\d+', temp)[0]

#uptime in seconds
def get_uptime(): 
	uptime = subprocess.check_output("cat /proc/uptime", shell=True)
	return float(uptime.split(" ")[0])

#returns load averages for 1, 5, and 15 minutes
def get_load_average():
	uptime = subprocess.check_output("uptime", shell=True)
	load_average = uptime.split("load average:")[1].split(",")
	return list(map(float, load_average))

def get_kernel_release():
	return subprocess.check_output("uname -r", shell=True)

def get_monitor_json():
	data = {
		"soc_temperature": get_soc_temperature(),
		"uptime": get_uptime(),
		"load_average": get_load_average(),
		"kernel_release": get_kernel_release()
		}
	json_value = json.dumps(data)
	return json_value

print(get_monitor_json())
