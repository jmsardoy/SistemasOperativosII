from flask.ext.wtf import Form
from wtforms import SubmitField, FileField, SelectField, PasswordField
from modules import getModules

class CommandsForm(Form):
	getTelemetry = SubmitField("Get Telemetry")
	getDatta = SubmitField("Get Datta")
	eraseDatta = SubmitField("Erase Datta")

class ModulesForm(Form):
	cargarModulo = SubmitField("Cargar Modulo")
	removerModulo = SubmitField("Remover Modulo")

class FileForm(Form):
	file = FileField("Elegir archivo")
	password = PasswordField("Contrasea")
	cargar = SubmitField("Cargar")

class RemoveForm(Form):
	select = SelectField(choices=[(i[0],i[0]) for i in getModules(1)])
	password = PasswordField("Contrasea")
	remove = SubmitField("Remover")

	def setChoices(self):
		self.select.choices = [(i[0],i[0]) for i in getModules(1)]