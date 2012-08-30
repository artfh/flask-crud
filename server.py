from flask import Flask
from flask import render_template,request, session, redirect, url_for


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XsH!jmN]LWX/,?RT'


user_list=[
	{ 'first_name':'Mark', 'last_name':'Otto', 'username':'@mdo'},
	{ 'first_name':'Jacob', 'last_name':'Thornton', 'username':'@fat'},
	{ 'first_name':'Larry the Bird', 'username':'@twitter'}
]

role_list=[
	{ 'name':'Administator', 'actions':'read,write'},
	{ 'name':'User', 'actions':'read'},
	{ 'name':'Developer', 'actions':'read,write,create'}
]

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/users")
def users():
	return render_template('users.html', rows=user_list)

@app.route("/roles")
def roles():
	return render_template('roles.html', rows=role_list)



if __name__ == "__main__":
	app.run(debug=True)