import fcntl

def getTelemetry():
	file = open("../datos/lastData.csv", "r")
	fcntl.flock(file, fcntl.LOCK_EX)
	telemetry = file.read()
	fcntl.flock(file, fcntl.LOCK_UN)
	file.close()
	telemetry = telemetry.replace("\n", "")
	telemetry = telemetry.split(",")
	if telemetry[0] != "":
		telemetry = [1] + telemetry
	telemetryList = [telemetry]
	return telemetryList

def getData():
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

def eraseData():
	file = open("../datos/dataGen.csv", "w")
	file.close()
	file = open("../datos/lastData.csv", "w")
	file.close()