import re
import subprocess
import os
from hashlib import md5

UPLOAD_PATH = "uploads"
PASSFILE = "passhash.psw"
PASSWORD = None
if os.path.exists(PASSFILE):
	PASSWORD = open(PASSFILE, "r").readline()

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

def saveFile(filename, file):
	file_path = UPLOAD_PATH+"/"+filename
	open(file_path,"w").write(file)

def insmod(modname, password):
	if(hash(password) == PASSWORD):
		file_path = UPLOAD_PATH+"/"+modname
		password = password+'\n'
		p = subprocess.Popen(["sudo", "-S", "insmod", file_path], stdin=subprocess.PIPE, 
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		response =  p.communicate(password)
		p.wait()
		if p.returncode==0:
			return (True,"Modulo instalado correctamente")
		else:
			output = response[1]
			return (False,"Hubo un error: "+output)
	else:
		return (False,"La clave es incorrecta")

def rmmod(modname, password):
	if(hash(password) == PASSWORD):
		password = password+'\n'
		p = subprocess.Popen(["sudo", "-S", "rmmod", modname], stdin=subprocess.PIPE, 
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		response =  p.communicate(password)
		p.wait()
		if p.returncode==0:
			return(True,"Modulo removido correctamente")
		else:
			output = response[1]
			return (False,"Hubo un error: "+output)
	else:
		return (False, "La clave es incorrecta")

def hash(password):
	m = md5(password)
	return m.digest()

if __name__ == "__main__":
	password = raw_input("Ingrese la clave: ")
	password = hash(password)
	open(PASSFILE,"w").write(password)
	print "Clave seteada con exito"
