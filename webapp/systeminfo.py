from datetime import timedelta
import platform

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