from flask import Flask, render_template, flash, request
from flask_bootstrap import Bootstrap
from werkzeug import secure_filename
import os

from commands import *
from forms import *

app = Flask(__name__)
Bootstrap(app)
UPLOAD_PATH = "uploads"
app.config['SECRET_KEY'] = "asflkg3opr"
app.config['UPLOAD_FOLDER'] = "uploads/"


@app.route("/")
def home():
	return render_template("home.html")

@app.route("/sysinfo")
def sysinfo():
	data = systemInfo()
	return render_template("system_info.html",data=data)



@app.route("/command", methods=['GET','POST'])
def commands():
	form = CommandsForm()
	data = None
	if form.validate_on_submit():
		if form.getTelemetry.data:
			data =  getTelemetry()
			if data[0][0] == '':
				flash("No hay datos", "danger")
		elif form.getDatta.data:
			data = getDatta()
			if not data:
				flash("No hay datos", "danger")
		elif form.eraseDatta.data:
			flash("Datos borrados", "success")
			eraseDatta()
	return render_template("commands.html", form=form, data=data)

@app.route("/modules", methods=['GET','POST'])
def modules():
	modulesForm = ModulesForm()
	fileForm = FileForm()
	removeForm = RemoveForm()
	modules = getModules(split=6)
	
	if fileForm.validate_on_submit() and fileForm.cargar.data:
		filename = fileForm.file.data.filename
		if validateFile(filename):
			file = request.files[fileForm.file.name].read()
			file_path = UPLOAD_PATH+"/"+filename
			open(file_path,"w").write(file)
			os.popen("sudo -S %s"%("insmod "+ file_path), 'w').write('holahola\n')
			modules = getModules(split=6)
			
		else:
			return "fileerror"
	
	if removeForm.validate_on_submit() and removeForm.remove.data:
		return "asdfasdg"

	return render_template("modules.html", modulesForm=modulesForm,modules=modules,
		fileForm=fileForm,removeForm=removeForm)

	


if __name__ == "__main__":
	app.debug = True
	app.run()