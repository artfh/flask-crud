import crud
from flask import request
import random

role_list1=[
    { 'id':1,'name':'Administator', 'actions':'read,write'},
    { 'id':2,'name':'User', 'actions':'read'},
    { 'id':3,'name':'Developer', 'actions':'read,write,create'}
]

user_list1=[
    { 'id':1, 'first_name':'Mark', 'last_name':'Otto', 'username':'@mdo'},
    { 'id':2, 'first_name':'Jacob', 'last_name':'Thornton', 'username':'@fat'},
    { 'id':3, 'first_name':'Larry the Bird', 'username':'@twitter'}
]

class Role(crud.Crud):

    name='role'
    objects=role_list1
    
    def formToModel(self, form, obj, isNew):
        obj['name']=request.form['name']
        obj['actions']=request.form['actions']
        if isNew:
            obj[self.pk_prop]=random.randint(0,100000)


class User(crud.Crud):

    name='user'
    objects=user_list1
    label_prop='username'
    
    def formToModel(self, form, obj, isNew):
        obj['first_name']=request.form['first_name']
        obj['last_name']=request.form['last_name']
        obj['username']=request.form['username']
        if isNew:
            obj[self.pk_prop]=random.randint(0,100000)




