# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 01:56:07 2020

@author: Srishti
"""


from datetime import datetime
from project import db, login_manager
from flask_login import UserMixin

#This class helps us to fulfill all the required criterias to login into an account like user_authentication or get_user_id etc.
#It will automatically be taken care of by 'UserMixin' at the time of authentication.

""" 
we use decorator so the extensions knows where a particular function is
 we will use this function to get a user (i.e. to load user information) from the database by it's user_id
"""
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # We will get back all the User Tuple using the get query.

"""
Now we will create a database structure or classes in here.
So each class is going to be a table in the database
"""

"""
Let's create the 'User' class first. 
Here, 'User' is the name of the table
"""
class User(db.Model, UserMixin):
    """
    Let us create coloumns
    Syntax:
        column_name = db.Column(db.Type, primary_key=True/False)
    """
    
    
    #First column is 'id'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    
    posts = db.relationship('Post', backref='author', lazy=True)
    #backref adds a coloumn to 'Post' module, it allows us to use the author attribute to know the user who posted it.
    #lazy 
    
    #We will also use __repr__ method called dunder methods or magic methods
    #This is usually used how object is printed whenever we print it out.
    # '__scr__' method also performs the same function.
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"