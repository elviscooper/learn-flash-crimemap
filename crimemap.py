import json
import string

from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
DB = DBHelper()


@app.route("/")
def home():	
	crimes = DB.get_all_crimes()
	crimes = json.dumps(crimes)
	return render_template("home.html", crimes=crimes)

@app.route("/add", methods=["POST"])
def add():
	try:
		data = request.form.get("userinput")
		DB.add_input(data)
	except Exception as e:
		print e
	return home()

@app.route("/clear")
def clear():
	try:
		DB.clear_all()
	except Exception as e:
		print e
	return home()

@app.route("/submitcrime", methods=['POST'])
def submitcrime():
	category = request.form.get("category")
	date = request.form.get("date")
	latitude = float(request.form.get("latitude"))
	longitude = float(request.form.get("longitude"))
	description = sanitize_string(request.form.get("description"))
	DB.add_crime(category, date, latitude, longitude, description)
	return home()

def sanitize_string(userinput):
    whitelist = string.letters + string.digits + " !?$.,;:-'()&"
    return filter(lambda x: x in whitelist, userinput)

if __name__ == '__main__':
	app.run(port=5000, debug=True)