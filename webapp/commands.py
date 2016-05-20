import fcntl
import platform
import re
from datetime import timedelta

def getTelemetry():
	file = open("../datos/lastData.csv", "r")
	fcntl.flock(file, fcntl.LOCK_EX)
	telemetry = file.read()
	fcntl.flock(file, fcntl.LOCK_UN)
	file.close()
	telemetry = telemetry.replace("\n", "")
	telemetry = telemetry.split(",")
	telemetryList = [telemetry]
	return telemetryList

def getDatta():
	file = open("../datos/dataGen.csv", "r")
	fcntl.flock(file, fcntl.LOCK_EX)
	data = file.read()
	fcntl.flock(file, fcntl.LOCK_UN)
	file.close()
	data =data.split("\n")
	for i,telemetry in enumerate(data):
		data[i] = telemetry.split(",")
	data.pop()
	return data

def eraseDatta():
	file = open("../datos/dataGen.csv", "w")
	file.close()
	file = open("..//datoslastData.csv","w")
	file.close()

def systemInfo():
	sysinfo = []
	t = ()
	for line in open("/proc/cpuinfo"):
		if line.startswith("model name"):
			t = ("CPU", line.split(":")[1])
			sysinfo.append(t)
			break;
	
	for line in open("/proc/meminfo"):
		if(line.startswith("MemTotal")):
			memorykb = line.split(":")[1].rstrip("\n").replace(" ", "")
			memorygb =''
			for i in memorykb:
				if(i.isdigit()):
					memorygb+=i
			memorygb = "%.2f Gb"% (float(memorygb)/1024/1024)
			t = ("Memoria", memorygb)
			sysinfo.append(t)
			break;
	for line in open("/proc/uptime"):
		t = ("Uptime", str(timedelta(seconds=int(line.split()[0].split(".")[0]))))
		sysinfo.append(t)
	t = ("Sistema Operativo", platform.system())
	sysinfo.append(t)
	t = ("Version del kernel", platform.version())
	sysinfo.append(t)

	return sysinfo

def getModules(split):
	modules = []
	for line in open("/proc/modules"):
		modules.append(line.split()[0])
	modules.sort()
	n = len(modules)/split
	if(len(modules)%split > 0):
		n = n+1
	modulesSplit = []
	for i in range(n):
		t = []
		for j in range(i,len(modules),n):
			t.append(modules[j])
		modulesSplit.append(t)


	return modulesSplit

def validateFile(filename):
	match = re.search("\.ko",filename)
	if match:
		return match.end()==len(filename)