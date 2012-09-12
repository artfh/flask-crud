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
    
    form=[
        {   'name':'name',
            'type':'text',
            'label':'Name'
        },
        {   'name':'actions',
            'type':'text',
            'label':'Actions'
        }
    ]
    


class User(crud.Crud):

    objects=user_list1

    name='user'
    label='User'
    label_prop='username'

    form=[
        {   'name':'first_name', 'type':'text','label':'First Name'   },
        {   'name':'last_name', 'type':'text','label':'Last Name'   },
        {   'name':'username', 'type':'text','label':'Username'   }     
    ]
    
   



