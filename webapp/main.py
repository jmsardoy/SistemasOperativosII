from flask import Flask, render_template, flash, request, redirect
from flask_bootstrap import Bootstrap
from werkzeug import secure_filename
from commands import *
from modules import *
from systeminfo import *
from forms import *
import sys


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = "asflkg3opr"

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

@app.route("/modules")
def modules():
	
	fileForm = FileForm()
	removeForm = RemoveForm()
	removeForm.setChoices()
	modulesForm = ModulesForm()
	modules = getModules(split=6)
	return render_template("modules.html", modulesForm=modulesForm,modules=modules,
		fileForm=fileForm,removeForm=removeForm)


@app.route("/insmod", methods=['POST'])
def insmodView():
	fileForm = FileForm()
	filename = fileForm.file.data.filename
	if validateFile(filename):
		file = request.files[fileForm.file.name].read()
		saveFile(file=file,filename=filename)
		password = fileForm.password.data
		result, output = insmod(modname=filename,password=password)
		if(result):
			flash(output,"success")
		else:
			flash(output,"danger")
	else:
		flash("Extension de archivo incorrecta", "danger")
	return redirect("/modules")

@app.route("/rmform", methods=['POST'])
def rmmodView():
	removeForm = RemoveForm()
	password = removeForm.password.data
	selectname = removeForm.select.data
	result, output = rmmod(modname=selectname, password=password)
	if(result):
		flash(output,"success")
	else:
		flash(output,"danger")
	return redirect("/modules")

if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0')