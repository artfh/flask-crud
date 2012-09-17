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

    objects=role_list1

    name='role'
    label='Role'
    
    fields={
        'name': {
            'label':'Name',
            'list_cell': 'href',
            'form_widget':'text'
        },
        'actions': {
            'label':'Actions',
            'form_widget':'text'
        }
    }

    list_columns=['name', 'actions']
    form=[ 'name', 'actions' ]

    


class User(crud.Crud):

    objects=user_list1

    name='user'
    label='User'
    label_prop='username'


    fields={
            'username': {
                'label':'Username',
                'list_cell': 'href'
            },
            'first_name': {
                'label':'First Name',
            },
            'last_name': {
                'label':'Last Name',
            }
        }
    list_columns=['username', 'first_name','last_name']
    form=[ 'first_name','last_name','username' ]
    
   


def createModel():
    app_model=crud.AppModel()
    app_model.project_name="My Project"
    app_model.add(User())
    app_model.add(Role())
    return app_model