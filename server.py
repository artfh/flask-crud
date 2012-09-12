from flask import Flask,current_app
from flask import render_template,request, session, redirect, url_for, flash

import random

import crud
import models.role




app = Flask(__name__)
with app.app_context():
    current_app.mystat='test123 '

app.secret_key = 'A0Zr98j/3yX R~XsH!jmN]LWX/,?RT'


model=models.role.createModel()
model.register(app)

@app.route("/")
def index():
	print current_app.mystat
	return render_template('index.html', app=model)





if __name__ == "__main__":
	app.run(debug=True)
