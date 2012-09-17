from flask import Flask,current_app
from flask import render_template,request, session, redirect, url_for, flash

import random

import crud
import models.role

import mymod
import yaml


app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XsH!jmN]LWX/,?RT'

with app.open_instance_resource('app.yaml') as f:
    conf = yaml.load(f.read())
    model=crud.AppModel(conf)
    model.register(app)
    print model.project_name


@app.route("/")
def index():
    print current_app.root_path,current_app.template_folder 
    return render_template('index.html', app=model)


app.register_blueprint(mymod.simple_page, url_prefix='/sp')



if __name__ == "__main__":
    app.run(debug=True)
