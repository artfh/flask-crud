from flask import Flask
from flask import render_template,request, session, redirect, url_for, flash

import random

import crud
import models.user



app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XsH!jmN]LWX/,?RT'


user_list=[
	{ 'id':1, 'first_name':'Mark', 'last_name':'Otto', 'username':'@mdo'},
	{ 'id':2, 'first_name':'Jacob', 'last_name':'Thornton', 'username':'@fat'},
	{ 'id':3, 'first_name':'Larry the Bird', 'username':'@twitter'}
]

role_list=[
	{ 'id':1,'name':'Administator', 'actions':'read,write'},
	{ 'id':2,'name':'User', 'actions':'read'},
	{ 'id':3,'name':'Developer', 'actions':'read,write,create'}
]

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/users", methods=['POST', 'GET'])
def users():

	if request.method == 'POST':
		user={}
		user['first_name']=request.form['first_name']
		user['last_name']=request.form['last_name']
		user['username']=request.form['username']
		user['id']=random.randint(0,100000)
		user_list.append(user)
		flash('User <strong>{username}</strong> created!'.format(username=user['username']))
		return redirect(url_for('users'))	

	return render_template('user/list.html', rows=user_list)

@app.route("/users/new")
def new_user():
	return render_template('user/new.html', obj={})	


@app.route("/users/del/<int:user_id>")
def delete_user(user_id):
	user = next(u for u in user_list if u['id'] == user_id)
	user_list.remove(user)
	flash('User <strong>{username}</strong> deleted!'.format(username=user['username']))
	return redirect(url_for('users'))	


@app.route("/users/<int:user_id>", methods=['POST', 'GET'])
def get_user(user_id):
	user = next(u for u in user_list if u['id'] == user_id)
	if request.method == 'POST':
		user['first_name']=request.form['first_name']
		user['last_name']=request.form['last_name']
		user['username']=request.form['username']	
		flash('User <strong>{username}</strong> updated!'.format(username=user['username']))
		return redirect(url_for('get_user', user_id=user_id))
	return render_template('user/edit.html', obj=user)	




@app.route("/roles")
def roles():
	return render_template('roles.html', rows=role_list)


#form=[ { 'name':'name', 'label':'Name', 'widget':'text',  }] 

c=crud.RoleCrud('role', objects=role_list, label_prop="name" )
c.navigation_hint='role.list'
c.register(app,'/role/')


if __name__ == "__main__":
	app.run(debug=True)
