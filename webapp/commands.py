import fcntl

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
		data[i] = [i+1] + telemetry.split(",")
	data.pop()
	return data

def eraseDatta():
	file = open("../datos/dataGen.csv", "w")
	file.close()
	file = open("../datos/lastData.csv", "w")
	file.close()