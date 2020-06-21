# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 02:10:06 2020

@author: Srishti
"""
""" initialize our application and bring together various components. """


from flask import Flask                  
"""
importing the Flask class 
"""

from flask_sqlalchemy import SQLAlchemy
"""
We imported the SQLAlchem class (Take care of the uppercase in the name of SQLAlchemy class)
After this we need to specify the URI of the database i.e. where the database is located.
Let's get started with SQLite database which will be a file on our file system and we set it's location as a configuration.
"""

from flask_bcrypt import Bcrypt

from  flask_login import LoginManager  # importing extensions in our app.


app = Flask(__name__)
"""                        
creating variable names app 
creating an instance of Flask class and passing argument __name__
 __name__ is a special variable in python
""" 


"""
To set config values on our application we use:
    app_name.config[]
    
    eg: To set a secret key , we have the following syntax:
        app.config['SECRET_KEY']=""
"""

"""
We need a secret key to protect our application against modifying cookies and cross-site request, forgery attacks etc.
The key must be some random characters, for which we will use the "secret" module in python
Syntax:
    import secrets
    secrets.token_hex(number_of_random_characters)
Example Code: 
    import secrets
    secrets.token_hex(16)
    
    Output: '3e574f2a7a35b8d429019f6836460594'
    
At some point , we need to make this an environment variable as well.
"""
app.config['SECRET_KEY'] = '3e574f2a7a35b8d429019f6836460594'



#app.config['SQLALCHEMY_DATABASE_URI']='mysql://{hr}:{1234}@localhost:5000/{db}'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
"""
Here we set a path for our database using SQLAlchemy
    1. If we use SQLite:
        Instead of an empty string we can specify a relative path with three forward slashes and a URI
        Syntax :
            app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
        Here these three forward slashes means the sqlite database file 'site.db' must be created in the same project folder
        where our application file 'project.py' is located.
"""

"""
Now, we need to create an instance of our database.
instance_variable = SQLAlchemy(name_of_app)
"""



db = SQLAlchemy(app)


bcrypt = Bcrypt(app)
""" Used to create hashed passwords to be stored in the database for securing the user lofin details. """

login_manager = LoginManager(app)
""" 
Used to manage login/logout user sessions.
We add functions to our database models and it will handle all of the sessions in the backgrounf for us
"""

login_manager.login_view = 'login' #function name of login route.
#shows login page when user tries to access any page that can only be accessed via being logged-in
login_manager.login_message_category = 'info' #bootstrap category for blue coloured info class.

from project import routes
