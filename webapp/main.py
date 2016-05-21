from flask import Flask, render_template, flash, request
from flask_bootstrap import Bootstrap
from werkzeug import secure_filename
from commands import *
from forms import *
import sys


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = "asflkg3opr"
PASSWORD = None

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
	
	fileForm = FileForm()
	if fileForm.validate_on_submit() and fileForm.cargar.data:
		filename = fileForm.file.data.filename
		if validateFile(filename):
			file = request.files[fileForm.file.name].read()
			saveFile(file=file,filename=filename)
			password = fileForm.password.data
			result, output = insmod(modname=filename,password=password,PASSWORD=PASSWORD)
			if(result):
				flash(output,"success")
			else:
				flash(output,"danger")
		else:
			flash("Extension de archivo incorrecta", "danger")

	removeForm = RemoveForm()
	if removeForm.validate_on_submit() and removeForm.remove.data:
		selectname = removeForm.select.data
		password = removeForm.password.data
		result, output = rmmod(modname=selectname, password=password,PASSWORD=PASSWORD)
		if(result):
			flash(output,"success")
		else:
			flash(output,"danger")

	removeForm.setChoices()
	modulesForm = ModulesForm()
	modules = getModules(split=6)
	return render_template("modules.html", modulesForm=modulesForm,modules=modules,
		fileForm=fileForm,removeForm=removeForm)


if __name__ == "__main__":
	if(len(sys.argv) > 1):
		PASSWORD = hash(sys.argv[1])
		app.debug = True
		app.run(host='0.0.0.0')
	else: 
		print "Debe ingresar la clave"
		sys.exit()